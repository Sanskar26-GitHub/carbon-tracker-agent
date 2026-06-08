from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import CarbonFootprintRequest, CarbonFootprintResponse
from app.services.calculator import CarbonCalculator

app = FastAPI(
    title="Carbon Tracker API",
    description="API for calculating personal carbon footprints deterministically.",
    version="1.0.0"
)

# 1. Mount the static directory so style.css and app.js can load
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Serve the index.html file when users visit the main URL
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# 3. The existing calculation engine endpoint
@app.post("/api/v1/calculate", response_model=CarbonFootprintResponse)
def calculate_carbon_footprint(request: CarbonFootprintRequest) -> CarbonFootprintResponse:
    """
    Calculate the carbon footprint based on transport, utility, and diet inputs.
    Delegates deterministic business logic to the CarbonCalculator service.
    """
    return CarbonCalculator.calculate_footprint(request)