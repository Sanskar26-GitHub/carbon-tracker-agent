"""
Configuration and constants for the carbon tracker application.
Centralizes all carbon emission factors as immutable float constants.
"""

# Vehicle emission factors (kg CO2e/km)
GASOLINE_SUV: float = 0.220
STANDARD_SEDAN: float = 0.170
HYBRID: float = 0.100
ELECTRIC_VEHICLE: float = 0.045
PUBLIC_BUS: float = 0.090

# Utility emission factors
GRID_ELECTRICITY_PER_KWH: float = 0.475
NATURAL_GAS_PER_CUBIC_METER: float = 1.93

# Diet emission profiles (kg CO2e/day)
MEAT_INTENSE: float = 7.20
AVERAGE_OMNIVORE: float = 5.40
VEGETARIAN: float = 3.80
VEGAN: float = 2.90
