from flask import request
from flask_restful import Resource
from utils.donate import HandleDonation

class TestDonations(Resource):
    def post(self):  # ✅ added self
        data = request.get_json()

        fundraiser_id = data.get('fundraiser_id') 
        message = data.get('message') 
        amount = data.get('amount') 
        donor_name = data.get('donor_name') 
        transaction_ref = data.get('transaction_ref') 
        print("testing")
        HandleDonation(
                fundraiser_id=fundraiser_id,
                amount=amount,
                message=message,
                donor_name=donor_name,
                transaction_ref=transaction_ref
            ).donate()

        # try:
        #     HandleDonation(
        #         fundraiser_id=fundraiser_id,
        #         amount=amount,
        #         message=message,
        #         donor_name=donor_name,
        #         transaction_ref=transaction_ref
        #     ).donate()
        #     return {"message": "Donation processed successfully"}, 200
        # except Exception as e:
        #     return {"error": str(e)}, 500
