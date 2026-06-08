"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from app.schemas import CarbonFootprintRequest, CarbonFootprintResponse
from app.services.calculator import CarbonCalculator

app = FastAPI(
    title="Carbon Tracker API",
    description="API for calculating personal carbon footprints deterministically.",
    version="1.0.0"
)

@app.post("/api/v1/calculate", response_model=CarbonFootprintResponse)
def calculate_carbon_footprint(request: CarbonFootprintRequest) -> CarbonFootprintResponse:
    """
    Calculate the carbon footprint based on transport, utility, and diet inputs.
    Delegates deterministic business logic to the CarbonCalculator service.
    """
    return CarbonCalculator.calculate_footprint(request)
