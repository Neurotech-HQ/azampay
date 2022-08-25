"""
AzamPay payment gateway Client SDK
"""

import re
import sys
import json
import requests
import logging
from json.decoder import JSONDecodeError
from typing import List, Dict, Optional, Any
from azampay.azampay_exceptions import (
    InvalidCredentials,
    BadRequest,
    InvalidURL,
    InternalServerError,
)

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class Azampay(object):
    """
    AzamPay payment gateway Client SDK
    """

    SANDBOX_AUTH_BASE_URL: str = "https://authenticator-sandbox.azampay.co.tz"
    SANDBOX_BASE_URL: str = "https://sandbox.azampay.co.tz"
    AUTH_BASE_URL: Optional[str] = None
    BASE_URL: Optional[str] = None

    SUPPORTED_MNOS: List[str] = ["Airtel", "Tigo", "Halopesa", "Azampesa"]
    SUPPORTED_BANKS: List[str] = ["CRDB", "NMB"]

    SUPPORTED_CURRENCIES: List[str] = ["TZS"]

    def __init__(
        self,
        *,
        app_name: str,
        client_id: str,
        client_secret: str,
        x_api_key: str,
        base_url: Optional[str] = None,
        auth_url: Optional[str] = None,
        sandbox: Optional[bool] = True,
    ):
        """__init__ method

        Initialize the AzamPay SDK with the app name, client id, client secret and base url.

        Args:
            app_name (str): The app name
            client_id (str): The client id
            client_secret (str): The client secret
            base_url (str, optional): Production base_url. Defaults to None.
            auth_url (str, optional): Production auth_base_url. Defaults to None.
            sandbox (bool, optional): determines whether you're running on sandbox or production url. Defaults to True.

        Raises:
            ValueError: When the mode is production and either base_url or auth_base_url is None

        Example:

        >>> from azampay import AzamPay
        >>> azampay = AzamPay(app_name='abc',client_id='xxx', client_secret='xyz', x_api_key='123')
        """
        if sandbox:
            self.AUTH_BASE_URL = self.SANDBOX_AUTH_BASE_URL
            self.BASE_URL = self.SANDBOX_BASE_URL
        else:
            if not (auth_url and base_url):
                raise ValueError(
                    "production auth_base_url and base_url are required in production mode"
                )

            self.AUTH_BASE_URL = auth_url
            self.BASE_URL = base_url

        self.app_name: str = app_name
        self.client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__token = self._token()
        self.__x_api_key = x_api_key

    def _token(self):
        token_url: str = f"{self.AUTH_BASE_URL}/AppRegistration/GenerateToken"
        response: Dict[str, Any] = self.post(
            url=token_url,
            body={
                "appName": self.app_name,
                "clientId": self.client_id,
                "clientSecret": self.__client_secret,
            },
            _headers=False,
        )
        token = response["data"]["accessToken"]
        message = response.get("message")
        logging.info(message)
        return token

    @property
    def headers(self) -> Dict[str, str]:
        """headers

        Returns:
            Dict[str, str]: Authenticated headers
        """
        return {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "application/json",
            "X-API-Key": self.__x_api_key,
        }

    def post(
        self, url: str, body: Dict[Any, Any], _headers: bool = True
    ) -> Dict[str, Any]:
        """post

        Makes easy to make a POST request with authenticated headers

        Args:
            url (str): The url to post to
            body (Dict[Any, Any]): JSON body of the request
            _headers (bool, optional): Determines where authenticated headers should be present or not. Defaults to True.

        Returns:
            Dict[str, Any]: JSON response from the server
        """
        if not _headers:
            response = requests.post(
                url=url,
                json=body,
                headers={"Content-Type": "application/json"},
            )
        else:
            response = requests.post(url=url, json=body, headers=self.headers)

        if response.status_code == 423:
            raise InvalidCredentials
        elif response.status_code == 400:
            raise BadRequest(f"Bad Request: {response.text}")
        elif response.status_code == 404:
            raise InvalidURL("{} is not a valid url".format(url))
        elif response.status_code == 500:
            raise InternalServerError
        else:
            try:
                return response.json()
            except ValueError as e:
                logging.error(e)
                return {
                    "message": "Something went wrong with decoding the response",
                    "status": response.status_code,
                    "data": response.text,
                }

    @staticmethod
    def clean_mobile_number(mobile_number: str) -> str:
        """clean_mobile_number

        Cleans the mobile number to remove any whitespace or dashes

        Args:
            mobile_number (str): The mobile number to clean

        Returns:
            str: The cleaned mobile number
        """

        # remove any non-numeric characters
        mobile_number = re.sub(r"[^0-9]", "", mobile_number)
        if len(mobile_number) < 9 or len(mobile_number) > 12:
            raise ValueError("Invalid mobile number")
        if len(mobile_number) == 9:
            mobile_number = f"255{mobile_number}"
        elif len(mobile_number) == 10:
            mobile_number = mobile_number.replace("0", "255", 1)
        return mobile_number

    @staticmethod
    def clean_amount(amount: str):
        # remove spaces and commas
        amount = str(amount)
        amount = amount.replace(" ", "").replace(",", "")
        return amount

    def mobile_checkout(
        self,
        *,
        mobile: str,
        amount: str,
        external_id: str,
        provider: str,
        currency: Optional[str] = "TZS",
        additional_properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """mobile_checkout : handles mobile checkout

        Args:
            mobile (str): This is the account number/MSISDN that consumer will provide. The amount will be deducted from this account.

            amount (str): This is amount that will be charged from the given account.

            external_id (str):This id belongs to the calling application

            provider (str): Enum: "Airtel" "Tigo" "Halopesa" "Azampesa"

            currency (Optional[str], optional):This is the transaciton currency. Current support values are only (TZS). Defaults to "TZS".

            additional_properties (Optional[Dict[str, Any]], optional): This is additional JSON data that calling application can provide. This is optional.. Defaults to None.

        Returns:
            Dict[str, Any]: The JSON response

        Example:
            add example here
        """

        # validate the provider
        mno_provider = provider.strip().capitalize()
        if mno_provider not in self.SUPPORTED_MNOS:
            raise ValueError(f"{mno_provider} is not a supported mno")

        # validate the currency
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"{currency} is not a supported currency")

        # clean the mobile number
        mobile = self.clean_mobile_number(mobile)

        # Clean the amount
        amount = self.clean_amount(amount)

        # Make info(f"Making request to {self.BASE_URL}/azampay/mno/checkout")
        response: Dict[str, Any] = self.post(
            url=f"{self.BASE_URL}/azampay/mno/checkout",
            body={
                "accountNumber": mobile,
                "amount": amount,
                "currency": currency,
                "externalId": external_id,
                "provider": mno_provider,
                "additionalProperties": additional_properties,
            },
        )
        message = response.get("message")
        logging.info(message)
        return response

    def bank_checkout(
        self,
        *,
        merchant_account_number: str,
        merchant_mobile_number: str,
        amount: str,
        otp: str,
        provider: str,
        reference_id: Optional[str] = None,
        currency: Optional[str] = "TZS",
        merchant_name: Optional[str] = None,
        additional_properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """bank_checkout : handle bank_checkout

        Args:
            merchant_account_number (str): This is the account number/MSISDN that consumer will provide. The amount will be deducted from this account.

            merchant_mobile_number str : Mobile number . Defaults to None.

            amount (str):This is amount that will be charged from the given account.

            otp (str): One time password

            provider (str): Bank provider Enum: "CRDB" "NMB"

            reference_id (Optional[str], optional): This id belongs to the calling application. Defaults to None.

            currency (Optional[str], optional): The currency code. Defaults to "TZS".

            merchant_name (Optional[str], optional): The name of consumer . Defaults to None.

            additional_properties (Optional[Dict[str, Any]], optional): This is additional JSON data that calling application can provide. This is optional. Defaults to None.

        Returns:
            Dict[str, Any]: _description_
        """

        ## validate the provider
        provider = provider.strip().upper()
        if provider not in self.SUPPORTED_BANKS:
            raise ValueError(f"{provider} is not a supported bank")

        # validate the currency
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"{currency} is not a supported currency")

        # clean the mobile number
        mobile = self.clean_mobile_number(merchant_mobile_number)

        # Clean the amount
        amount = self.clean_amount(amount)

        ## Makeinfo(f"Making request to {self.BASE_URL}/azampay/bank/checkout")
        response: Dict[str, Any] = self.post(
            f"{self.BASE_URL}/azampay/bank/checkout",
            body={
                "amount": amount,
                "currencyCode": currency,
                "merchantAccountNumber": merchant_account_number,
                "merchantMobileNumber": mobile,
                "merchantName": merchant_name,
                "otp": otp,
                "provider": provider,
                "referenceId": reference_id,
                "additionalProperties": additional_properties,
            },
        )

        logging.info(response)
        message = response.get("message")
        logging.info(message)
        return response


# sys.modules[__name__] = Azampay
