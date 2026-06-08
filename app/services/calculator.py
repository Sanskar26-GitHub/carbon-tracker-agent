"""
Business logic for carbon footprint calculations.
"""
from typing import List
from app import config
from app.schemas import CarbonFootprintRequest, CarbonFootprintResponse

class CarbonCalculator:
    """Service class for calculating carbon footprints."""

    @staticmethod
    def calculate_footprint(request: CarbonFootprintRequest) -> CarbonFootprintResponse:
        """
        Calculate total carbon footprint deterministically in O(1) time complexity.
        """
        # 1. Transport Emissions
        vehicle_factors: dict[str, float] = {
            "suv": config.GASOLINE_SUV,
            "sedan": config.STANDARD_SEDAN,
            "hybrid": config.HYBRID,
            "ev": config.ELECTRIC_VEHICLE,
            "bus": config.PUBLIC_BUS,
        }
        factor = vehicle_factors[request.vehicle_type]
        
        # Carpool logic
        if request.carpool_passengers > 0:
            efficiency_correction = 1.0 - (1.0 / (request.carpool_passengers + 1.0))
        else:
            efficiency_correction = 0.0
            
        transport_emissions = (request.transport_distance_km * factor) * (1.0 - efficiency_correction)
        
        # 2. Utility Emissions
        utility_emissions = (request.electricity_kwh * config.GRID_ELECTRICITY_PER_KWH) + \
                            (request.natural_gas_m3 * config.NATURAL_GAS_PER_CUBIC_METER)
                            
        # 3. Diet Emissions
        diet_factors: dict[str, float] = {
            "meat_intense": config.MEAT_INTENSE,
            "omnivore": config.AVERAGE_OMNIVORE,
            "vegetarian": config.VEGETARIAN,
            "vegan": config.VEGAN,
        }
        diet_emissions = diet_factors[request.diet_profile]
        
        total_emissions = transport_emissions + utility_emissions + diet_emissions
        
        # 4. Insights Generation
        insights = CarbonCalculator._generate_insights(
            transport_emissions, 
            utility_emissions, 
            diet_emissions
        )
        
        return CarbonFootprintResponse(
            transport_emissions=round(transport_emissions, 2),
            utility_emissions=round(utility_emissions, 2),
            diet_emissions=round(diet_emissions, 2),
            total_emissions=round(total_emissions, 2),
            insights=insights
        )

    @staticmethod
    def _generate_insights(transport: float, utility: float, diet: float) -> List[str]:
        """Generate exactly 3 dynamic insights based on the highest emission category."""
        insights: List[str] = []
        highest = max(transport, utility, diet)
        
        if highest == transport and transport > 0:
            insights.append("Transport is your highest emission category.")
            insights.append("Consider carpooling or switching to a hybrid or electric vehicle.")
            insights.append("Using public transit can also significantly reduce your carbon footprint.")
        elif highest == utility and utility > 0:
            insights.append("Home utilities are your highest emission category.")
            insights.append("Consider switching to renewable energy sources if possible.")
            insights.append("Improving home insulation and reducing electricity usage will lower these emissions.")
        elif highest == diet and diet > 0:
            insights.append("Your diet is your highest emission category.")
            insights.append("Consider incorporating more plant-based meals into your routine.")
            insights.append("Reducing meat consumption, particularly beef, has a major positive environmental impact.")
        else:
            insights.append("Your emissions are exceptionally low across all categories.")
            insights.append("Keep up the great work maintaining a sustainable lifestyle.")
            insights.append("Consider sharing your habits with others to amplify your impact.")
            
        return insights
