"""
Azampay Callback Example  
"""

import logging
from pydantic import BaseModel
from typing import Optional, Any, Dict
from fastapi import FastAPI, Request


# Setup logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Setup FastAPI

app = FastAPI()


# Define the callback model


class Callback(BaseModel):
    """Callback Model

    Example:

    ```json
    {
        'msisdn':'0178823','amount':'2000',
        'message':'any message','utilityref':
        '1292-123','operator':'Tigo','reference':'123-123',
        'transactionstatus':'success','submerchantAcc':'01723113'
    }

    """

    msisdn: str
    amount: str
    message: str
    utilityref: str
    operator: str
    reference: str
    transactionstatus: str
    submerchantAcc: str
    additionalProperties: Optional[Dict[Any, Any]] = None


# Define the callback endpoint
# This endpoint will be called by Azampay
# when a transaction is completed or failed


@app.post("/api/v1/Checkout/Callback")
async def callback(request: Request):
    callback = await request.json()
    logging.info(f"Callback: {callback}")
    return {"status": "success"}


# Run the app
# uvicorn callback:app --reload
