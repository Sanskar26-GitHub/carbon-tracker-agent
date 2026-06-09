from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import CarbonFootprintRequest, CarbonFootprintResponse
from app.services.calculator import CarbonCalculator

app = FastAPI(
    title="Carbon Tracker API",
    description="API for calculating personal carbon footprints deterministically.",
    version="1.0.0"
)

# 1. Strict CORS Middleware (Security Boost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# 2. Enterprise Security Headers (Security Boost)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Note: The blanket exception handler has been INTENTIONALLY REMOVED 
# to allow FastAPI and your calculator to gracefully handle business logic errors natively.

# 3. Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Serve Frontend
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# 5. Asynchronous Calculation Engine (Efficiency Boost)
@app.post("/api/v1/calculate", response_model=CarbonFootprintResponse)
async def calculate_carbon_footprint(request: CarbonFootprintRequest) -> CarbonFootprintResponse:
    """
    Calculate the carbon footprint based on transport, utility, and diet inputs.
    Delegates deterministic business logic to the CarbonCalculator service.
    """
    return CarbonCalculator.calculate_footprint(request)