"""
Automated testing suite for the Carbon Tracker API.
Validates mathematical accuracy and strict boundary logic.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_baseline_standard_input():
    """
    Test 1: Baseline standard input.
    Verifies that standard inputs return a 200 OK and exactly match mathematical expectations.
    """
    payload = {
        "transport_distance_km": 10.0,
        "vehicle_type": "sedan",
        "carpool_passengers": 0,
        "electricity_kwh": 10.0,
        "natural_gas_m3": 5.0,
        "diet_profile": "omnivore"
    }
    
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Expected Calculations:
    # Transport (sedan = 0.170): 10 * 0.170 = 1.7
    # Utilities: (10 * 0.475) + (5 * 1.93) = 4.75 + 9.65 = 14.4
    # Diet (omnivore = 5.40): 5.4
    # Total: 1.7 + 14.4 + 5.4 = 21.5
    
    assert data["transport_emissions"] == 1.7
    assert data["utility_emissions"] == 14.4
    assert data["diet_emissions"] == 5.4
    assert data["total_emissions"] == 21.5

def test_carpool_logic_reduction():
    """
    Test 2: Carpool logic reduction.
    Verifies that 3 carpool passengers reduce emissions by exactly 75%.
    """
    payload = {
        "transport_distance_km": 10.0,
        "vehicle_type": "suv",
        "carpool_passengers": 3,
        "electricity_kwh": 0.0,
        "natural_gas_m3": 0.0,
        "diet_profile": "vegan"
    }
    
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # Base transport (suv = 0.220): 10 * 0.220 = 2.2
    # Passengers = 3 -> efficiency_correction = 1 - 1/(3+1) = 0.75
    # Adjusted transport: 2.2 * (1 - 0.75) = 2.2 * 0.25 = 0.55
    
    assert data["transport_emissions"] == 0.55

def test_negative_inputs_validation():
    """
    Test 3: Negative inputs.
    Verifies that Pydantic properly blocks negative distance inputs with a 422 error.
    """
    payload = {
        "transport_distance_km": -10.0,
        "vehicle_type": "sedan",
        "carpool_passengers": 0,
        "electricity_kwh": 10.0,
        "natural_gas_m3": 5.0,
        "diet_profile": "omnivore"
    }
    
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 422

def test_invalid_literal_strings_validation():
    """
    Test 4: Invalid literal strings.
    Verifies that Pydantic blocks unapproved string literals with a 422 error.
    """
    payload = {
        "transport_distance_km": 10.0,
        "vehicle_type": "sedan",
        "carpool_passengers": 0,
        "electricity_kwh": 10.0,
        "natural_gas_m3": 5.0,
        "diet_profile": "carnivore"  # 'carnivore' is not in the approved Literal set
    }
    
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 422

def test_zero_values():
    """
    Test 5: Zero values.
    Verifies that passing zero to all scalable inputs runs safely without division-by-zero errors.
    """
    payload = {
        "transport_distance_km": 0.0,
        "vehicle_type": "ev",
        "carpool_passengers": 0,
        "electricity_kwh": 0.0,
        "natural_gas_m3": 0.0,
        "diet_profile": "vegan"
    }
    
    response = client.post("/api/v1/calculate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["transport_emissions"] == 0.0
    assert data["utility_emissions"] == 0.0
    assert data["diet_emissions"] == 2.9  # Vegan base profile
    assert data["total_emissions"] == 2.9
