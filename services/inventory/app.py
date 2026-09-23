from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
import uuid

app = FastAPI(
    title="Inventory Service",
    version="1.0.0"
)

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL",
    "http://localhost:8003"
)


class ReserveRequest(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    amount: float


class ReserveResponse(BaseModel):
    reservation_id: str
    order_id: str
    product_id: str
    quantity: int
    payment_status: str
    status: str


@app.get("/health")
def health():
    return {
        "service": "inventory",
        "status": "healthy"
    }


@app.post("/reserve", response_model=ReserveResponse)
async def reserve_inventory(request: ReserveRequest):

    if request.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    payment_payload = {
        "order_id": request.order_id,
        "amount": request.amount
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{PAYMENT_SERVICE_URL}/authorize",
                json=payment_payload
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Payment service failed"
            )

        payment_data = response.json()

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Payment service unavailable: {exc}"
        )

    reservation_id = f"res-{uuid.uuid4().hex[:12]}"

    return ReserveResponse(
        reservation_id=reservation_id,
        order_id=request.order_id,
        product_id=request.product_id,
        quantity=request.quantity,
        payment_status=payment_data["status"],
        status="reserved"
    )