import os
from azampay import Azampay
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AzamPay
gateway = Azampay(
    app_name=os.getenv("APP_NAME"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    x_api_key=os.getenv("X_API_KEY"),
)

# >>> checkout_response = azampay.bank_checkout(amount=100, merchant_account_number='<merchant_account_number>', merchant_mobile_number='<merchant_mobile_number>', reference_id='<external_id>', provider='<provider>'
# response = gateway.mobile_checkout(
#     mobile="0657649154", amount=1000, provider="tigo", external_id="123456789"
# )
checkout_response = gateway.bank_checkout(
    amount=100,
    merchant_account_number="123456789",
    merchant_mobile_number="0657649154",
    reference_id="123456789",
    otp="123456",
    provider="NMB",
)
print(checkout_response)
