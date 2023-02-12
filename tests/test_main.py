import os
import uuid
import pytest
from azampay import Azampay
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AzamPay
@pytest.fixture
def gateway():
    return Azampay(
        app_name=os.getenv("APP_NAME"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        x_api_key=os.getenv("X_API_KEY"),
    )


def test_bank_checkout(gateway):
    reference_id = str(uuid.uuid4())
    checkout_response = gateway.bank_checkout(
        amount=100,
        merchant_account_number="123456789",
        merchant_mobile_number="0657649154",
        reference_id=reference_id,
        otp="123456",
        provider="NMB",
    )
    print(checkout_response)
    assert isinstance(checkout_response, dict)
    assert checkout_response["success"] == True
    assert isinstance(checkout_response["transactionId"], str)


def test_mobile_checkout(gateway):
    reference_id = str(uuid.uuid4())
    checkout_response = gateway.mobile_checkout(
        mobile="0667863412", amount=1000, provider="tigo", external_id=reference_id
    )

    print(checkout_response)
    assert isinstance(checkout_response, dict)
    assert checkout_response["success"] == True
    assert isinstance(checkout_response["transactionId"], str)
