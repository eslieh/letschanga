import json
from utils.donate import HandleDonation

# Load the test data from JSON file
with open('donation_data.json', 'r') as file:
    data = json.load(file)

# Extract fields
fundraiser_id = data.get('fundraiser_id')
amount = data.get('amount')
message = data.get('message')
donor_name = data.get('donor_name')
transaction_ref = data.get('transaction_ref')

# Call the HandleDonation class directly
try:
    result = HandleDonation(fundraiser_id, amount, message, donor_name, transaction_ref).donate()
    print("Donation processed:", result)
except Exception as e:
    print("Donation failed with error:", str(e))
