from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
import uuid

from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Checkout Service",
    version="1.0.0"
)

INVENTORY_SERVICE_URL = os.getenv(
    "INVENTORY_SERVICE_URL",
    "http://localhost:8002"
)


class CheckoutRequest(BaseModel):
    product_id: str
    quantity: int
    amount: float


class CheckoutResponse(BaseModel):
    order_id: str
    reservation_id: str
    payment_status: str
    status: str


@app.get("/health")
def health():
    return {
        "service": "checkout",
        "status": "healthy"
    }


@app.post("/checkout", response_model=CheckoutResponse)
async def checkout(request: CheckoutRequest):
    if request.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    order_id = f"order-{uuid.uuid4().hex[:12]}"

    inventory_payload = {
        "order_id": order_id,
        "product_id": request.product_id,
        "quantity": request.quantity,
        "amount": request.amount
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{INVENTORY_SERVICE_URL}/reserve",
                json=inventory_payload
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Inventory service failed"
            )

        inventory_data = response.json()

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Inventory service unavailable: {exc}"
        )

    return CheckoutResponse(
        order_id=order_id,
        reservation_id=inventory_data["reservation_id"],
        payment_status=inventory_data["payment_status"],
        status="completed"
    )


Instrumentator().instrument(app).expose(app)
