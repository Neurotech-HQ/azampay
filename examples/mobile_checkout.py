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


response = gateway.mobile_checkout(
    mobile="06xxxxxxxx", amount=1000, provider="tigo", external_id="123456789"
)

print(response)
