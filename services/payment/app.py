from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import time

app = FastAPI(
    title="Payment Service",
    version="1.0.0"
)


class PaymentRequest(BaseModel):
    order_id: str
    amount: float


class PaymentResponse(BaseModel):
    payment_id: str
    order_id: str
    status: str
    amount: float


@app.get("/health")
def health():
    return {
        "service": "payment",
        "status": "healthy"
    }


@app.post("/authorize", response_model=PaymentResponse)
def authorize_payment(request: PaymentRequest):
    payment_id = f"pay-{uuid4().hex[:12]}"

    # Simulated payment processing time.
    time.sleep(0.05)

    return PaymentResponse(
        payment_id=payment_id,
        order_id=request.order_id,
        status="authorized",
        amount=request.amount
    )