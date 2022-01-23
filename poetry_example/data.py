from pydantic import BaseModel


class CalculationRequest(BaseModel):
    x: int
    y: float


class CalculationResponse(BaseModel):
    result: float
