from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import time
import os

from prometheus_fastapi_instrumentator import Instrumentator


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


failure_mode = "normal"


@app.get("/health")
def health():
    return {
        "service": "payment",
        "status": "healthy"
    }


@app.get("/control/status")
def control_status():
    return {
        "service": "payment",
        "failure_mode": failure_mode
    }


@app.post("/control/failure")
def control_failure(payload: dict):
    global failure_mode

    mode = payload.get("mode", "normal")

    if mode not in {"normal", "payment_error", "payment_slow"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid failure mode"
        )

    failure_mode = mode

    return {
        "service": "payment",
        "failure_mode": failure_mode
    }


@app.post("/authorize", response_model=PaymentResponse)
def authorize_payment(request: PaymentRequest):
    if failure_mode == "payment_error":
        raise HTTPException(
            status_code=500,
            detail="Simulated payment failure"
        )

    if failure_mode == "payment_slow":
        time.sleep(2.0)
    else:
        time.sleep(0.05)

    payment_id = f"pay-{uuid4().hex[:12]}"

    return PaymentResponse(
        payment_id=payment_id,
        order_id=request.order_id,
        status="authorized",
        amount=request.amount
    )


Instrumentator().instrument(app).expose(app)
