<samp>

# [azampay](https://developerdocs.azampay.co.tz/redoc)

Python Wrapper to Azampay Payment Gateway

## Azampay API Flow

All Azampay APIs follow two step process:

Step 1: Get token against the application authentication credentials.
Step 2: Consume the actual api by providing x-api-key header and token acquired in step 1.
Following diagram shows the general flow on how to consume the Azampay api.

![Azam Pay](https://developerdocs.azampay.co.tz/flow-diagrams/checkout-flow.svg)


## Getting Started

To get started with Azampay, you need to install the azampay package. You can either do it manually or use pip to install it.

### Manual Installation

```bash
$ git clone https://github.com/Neurotech-HQ/azampay
$ cd azampay
$ sudo python setup.py install
```

### Using pip

```bash
$ pip install azampay
```

## Authentication

Azampay offers two forms of authentication:

### API Key

Bearer Auth - an open protocol to allow secure authorization in a simple and standard method from web, mobile and desktop applications.
API-Key is the key that is provided in the http request header. Key Name is X-API-KEY.

```Bearer Token``` is the JWT token that you get against your application Name, Client Id and Client Secret. For Sanbox Environment, You can get these application credentials from Sandbox portal. For production environment, you will be provided these keys after you submit your business KYC to Azampay from Sandbox portal.

**Azampay** Package handles the authentication for you. You just need to provide it with its credentials and it will do the rest. Here is the example of how to use it.

```python
>>> from azampay import Azampay
>>> azampay = Azampay(app_name='<app_name'>, client_id='<client_id>', client_secret='<client_secret>', x_api_key='<x_api_key>', sandbox=True)
```

**Note**: When you want to use the package in production environment, you will need to provide the production credentials provided by Azampay plus the  production base and authentication endpoints. Here is the example of how to use it.

```python

>>> from azampay import Azampay
>>> azampay = Azampay(app_name='<app_name>', client_id='<client_id>', client_secret='<client_secret>', x_api_key='<x_api_key>', sandbox=False, base_url='<base_url>', auth_url='<auth_url>')
```

## Checkout

Azampay offers two types of checkout:

1. Mobile Checkout - for mobile checkout (Tigopesa, AirtelMoney, Mpesa)
2. Bank Checkout - for bank checkout (CRDB, NMB)

### Mobile Checkout

Here is the example of how to use the mobile checkout.

```python
>>> from azampay import Azampay
>>> azampay = Azampay(app_name='<app_name>', client_id='<client_id>', client_secret='<client_secret>', x_api_key='<x_api_key>', sandbox=True)
>>> checkout_response = azampay.mobile_checkout(amount=100, mobile='<mobile>', external_id='<external_id>', provider='<provider>')
```

### Bank Checkout

Here is the example of how to use the bank checkout.

```python
>>> from azampay import Azampay
>>> azampay = Azampay(app_name='<app_name>', client_id='<client_id>', client_secret='<client_secret>', x_api_key='<x_api_key>', sandbox=True)
>>> checkout_response = azampay.bank_checkout(amount=100, merchant_account_number='<merchant_account_number>', merchant_mobile_number='<merchant_mobile_number>', external_id='<external_id>', provider='<provider>')
```

### Callback

Now that you already know to initiate payments with Azampay package, Let's get started with the callback.

>_Note_: You will need to have a webhook endpoint set up on your application to receive the callback from Azampay.

I have added a starter [FastAPI webhook endpoint](https://github.com/Neurotech-HQ/azampay/blob/main/callback.py) to this repository. You can either use it or set up your own.

#### Webhook Data

Here an example of the webhook data that you will receive from Azampay.

```json
{
    "msisdn": "0178823",
    "amount": "2000",
    "message": "any message",
    "utilityref": "1292-123",
    "operator": "Tigo",
    "reference": "123-123",
    "transactionstatus": "success",
    "submerchantAcc": "01723113",
}
```

## Issues

If you will face any issue with the usage of this package please raise one so as we can quickly fix it as soon as possible;

## Contributing

This is an opensource project under ```MIT License``` so any one is welcome to contribute from typo, to source code to documentation, ```JUST FORK IT```.

## Related

1. [Python-DPO](https://github.com/Neurotech-HQ/python-dpo)
2. [Pypesa](https://github.com/Neurotech-HQ/pypesa)
3. [Tigopesa](https://github.com/Neurotech-HQ/tigopesa)

## All the credit

1. [kalebu](https://github.com/Kalebu)
2. All other contributors


</samp>
