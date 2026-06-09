from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.schemas import CarbonFootprintRequest, CarbonFootprintResponse
from app.services.calculator import CarbonCalculator

app = FastAPI(
    title="Carbon Tracker API",
    description="API for calculating personal carbon footprints deterministically.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# 1. Mount the static directory so style.css and app.js can load
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Serve the index.html file when users visit the main URL
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# 3. The existing calculation engine endpoint
@app.post("/api/v1/calculate", response_model=CarbonFootprintResponse)
async def calculate_carbon_footprint(request: CarbonFootprintRequest) -> CarbonFootprintResponse:
    """
    Calculate the carbon footprint based on transport, utility, and diet inputs.
    Delegates deterministic business logic to the CarbonCalculator service.
    """
    return CarbonCalculator.calculate_footprint(request)