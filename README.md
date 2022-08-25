<samp>

# azampay

Python Wrapper to Azampay Payment Gateway

## Base Urls

Authenticator Sandbox Base Url: <https://authenticator-sandbox.azampay.co.>.
Azampay Sandbox Checkout Base Url: <https://sandbox.azampay.co.tz>.

## Azampay API Flow

All Azampay APIs follow two step process:

Step 1: Get token against the application authentication credentials.
Step 2: Consume the actual api by providing x-api-key header and token acquired in step 1.
Following diagram shows the general flow on how to consume the Azampay api.

![Azam Pay](https://developerdocs.azampay.co.tz/flow-diagrams/checkout-flow.svg)

## Authentication

Azampay offers two forms of authentication:

### API Key

Bearer Auth - an open protocol to allow secure authorization in a simple and standard method from web, mobile and desktop applications.
API-Key is the key that is provided in the http request header. Key Name is X-API-KEY.

```Bearer Token``` is the JWT token that you get against your application Name, Client Id and Client Secret. For Sanbox Environment, You can get these application credentials from Sandbox portal. For production environment, you will be provided these keys after you submit your business KYC to Azampay from Sandbox portal.


</samp>