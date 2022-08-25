"""
Azampay Callback Example  
"""

import logging
from fastapi import FastAPI, Request

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Define the callback endpoint
# This endpoint will be called by Azampay
# when a transaction is completed or failed


@app.post("/api/v1/Checkout/Callback")
async def callback(request: Request):
    _callback_data = await request.json()
    logging.info(f"Callback: {_callback_data}")
    return {"status": "success"}


# Run the application
# uvicorn callback:app --reload
