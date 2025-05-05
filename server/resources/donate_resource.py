from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from models import db
from models.donation import Donation
from models.fundraiser import Fundraiser
import base64
import requests
import os

from utils.donate import HandleDonation
class Donate_resource(Resource):
    def post(self):
        data =  request.get_json()
        
        fundraiser_id = data.get('fundraiser_id') 
        message = data.get('message') 
        amount = int(data.get('amount')) 
        donor_name = data.get('donor_name') 
        mpesa_number = data.get('mpesa_number')
        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id).first()
        if not fundraiser:    
            return {"error":"no fundraiser found"}, 403    
        
        
        
        consumer_key = os.getenv('SAFARICOM_SANDBOX_CONSUMER_KEY')
        consumer_secret = os.getenv('SAFARICOM_SANDBOX_CONSUMER_SECRET')
        shortcode = os.getenv('SAFARICOM_SANDBOX_SHORTCODE')
        passkey = os.getenv('SAFARICOM_SANDBOX_PASSKEY')
        callback_url = "https://bgrtfdl5-5000.uks1.devtunnels.ms/api/callback/mpesa/donation"

        # Encode credentials
        credentials = f"{consumer_key}:{consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Token URL
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        # Get access token
        auth_headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        auth_response = requests.get(auth_url, headers=auth_headers)
        if auth_response.status_code != 200:
            return {"error": "Failed to get M-Pesa token"}, 500

        access_token = auth_response.json().get("access_token")
        print("tokcn recieved")
        # Step 2: Send STK Push
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

        def normalize_mpesa_number(mpesa_number):
            mpesa_number = str(mpesa_number).strip()

            # Remove '+' if present
            if mpesa_number.startswith('+'):
                mpesa_number = mpesa_number[1:]

            # If number starts with 0, replace with 254
            if mpesa_number.startswith('0'):
                mpesa_number = '254' + mpesa_number[1:]

            # If number starts with 7 or 1, assume it's missing 254
            if mpesa_number.startswith(('7', '1')) and len(mpesa_number) == 9:
                mpesa_number = '254' + mpesa_number

            # Validate final length
            if not mpesa_number.startswith('254') or len(mpesa_number) != 12:
                raise ValueError("Invalid Mpesa number format.")

            return mpesa_number
        callback_url = "https://bgrtfdl5-5000.uks1.devtunnels.ms/api/callback/mpesa/donation"
        normalized_number = int(normalize_mpesa_number(mpesa_number)) 
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": normalized_number,
            "PartyB": shortcode,
            "PhoneNumber": normalized_number,
            "CallBackURL": callback_url,
            "AccountReference": fundraiser.title,
            "TransactionDesc": "Donation"
        }
        print(payload)
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            donation = Donation(amount=amount, message=message, donor_name=donor_name, fundraiser_id=fundraiser_id, merchant_request_id= data.get('CheckoutRequestID'))
            db.session.add(donation)
            db.session.commit()
            return{"success":"initiated successfully", "data": "hello"}
        else:
            print("Error initiating STK Push:", response.status_code, response.text)
            return {"error": f"Error initiating STK Push: {response.status_code}, {response.text}"}, 400

class Donatio_callBack(Resource):
    def post(self):
        data = request.get_json()
        print("Callback Received:", data)

        try:
            stk = data['Body']['stkCallback']
            merchant_request_id = stk.get('MerchantRequestID')
            checkout_request_id = stk.get('CheckoutRequestID')
            result_code = stk.get('ResultCode')
            result_desc = stk.get('ResultDesc')

            metadata = stk.get('CallbackMetadata', {}).get('Item', [])
            parsed_metadata = {item['Name']: item.get('Value') for item in metadata}

            amount = parsed_metadata.get("Amount")
            mpesa_receipt_number = parsed_metadata.get("MpesaReceiptNumber")
            transaction_date = parsed_metadata.get("TransactionDate")
            phone_number = parsed_metadata.get("PhoneNumber")


            # # Fetch matching donation by checkout_request_id
            donation = Donation.query.filter_by(merchant_request_id=checkout_request_id).first()

            if not donation:
                return {"error": "Donation not found"}, 404

            # Update donation status based on result_code
            if result_code == 0:
                donation.status = "success"
                donation.donated = True
                donation.amount = amount
                donation.transaction_ref = mpesa_receipt_number
                db.session.commit()
                HandleDonation(
                    fundraiser_id=donation.fundraiser_id,
                    amount=amount,
                    message = donation.message,
                    donor_name= donation.donor_name,
                    transaction_ref=mpesa_receipt_number
                ).donate()
            else:
                donation.status = "Failed"
                db.session.commit()
            
            return {"message": "Callback processed successfully"}, 200

        except Exception as e:
            print("Error processing callback:", str(e))
            return {"message": "Invalid callback payload"}, 400