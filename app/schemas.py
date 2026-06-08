"""
Pydantic schemas for request and response validation.
"""
from typing import List, Literal
from pydantic import BaseModel, Field

class CarbonFootprintRequest(BaseModel):
    transport_distance_km: float = Field(
        ..., 
        ge=0.0, 
        description="Transport distance in kilometers"
    )
    vehicle_type: Literal["suv", "sedan", "hybrid", "ev", "bus"] = Field(
        ..., 
        description="Type of vehicle used"
    )
    carpool_passengers: int = Field(
        ..., 
        ge=0, 
        description="Number of carpool passengers"
    )
    electricity_kwh: float = Field(
        ..., 
        ge=0.0, 
        description="Electricity consumption in kWh"
    )
    natural_gas_m3: float = Field(
        ..., 
        ge=0.0, 
        description="Natural gas consumption in cubic meters"
    )
    diet_profile: Literal["meat_intense", "omnivore", "vegetarian", "vegan"] = Field(
        ..., 
        description="Dietary profile"
    )

class CarbonFootprintResponse(BaseModel):
    transport_emissions: float = Field(..., description="Emissions from transport in kg CO2e")
    utility_emissions: float = Field(..., description="Emissions from utilities in kg CO2e")
    diet_emissions: float = Field(..., description="Emissions from diet in kg CO2e")
    total_emissions: float = Field(..., description="Total carbon footprint in kg CO2e")
    insights: List[str] = Field(..., description="List of personalized insights and recommendations")
