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
    base_url="https://checkout.azampay.co.tz",
    auth_url="https://authenticator.azampay.co.tz",
    sandbox=False,
)


response = gateway.mobile_checkout(
    mobile="255657649154", amount=1000, external_id="123456789"
)

print(response)
