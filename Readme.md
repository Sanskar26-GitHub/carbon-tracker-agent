# 🌍 EcoPulse: Personal Carbon Intelligence Agent

## 1. Chosen Vertical & Persona
**Persona:** Personal Sustainability Assistant.
This platform is designed to help individuals understand, track, and reduce their daily carbon footprint through simple, deterministic data entry and actionable, localized insights.

## 2. Approach & Logic
EcoPulse utilizes a microservice architecture built for maximum efficiency and security:
* **Backend (FastAPI):** A deterministic, $O(1)$ calculation engine that avoids loops and complex matrix arrays, relying instead on pure dictionary lookups and standardized float constants.
* **Frontend (Vanilla JS):** An ultra-lightweight, WCAG 2.1 AA compliant Single-Page Application (SPA) that operates without heavy external DOM libraries to ensure ultra-fast load times.
* **Security:** All payload validations are strictly enforced at the Pydantic boundary layer to prevent malicious data injection. DOM rendering uses `textContent` to neutralize XSS risks.

## 3. How It Works
1. A user inputs their daily transport, utility, and dietary data into the accessible interface.
2. The UI sends a secure JSON payload to the `/api/v1/calculate` endpoint.
3. The deterministic calculation engine evaluates the parameters against configured baseline factors.
4. The API returns real-time emission metrics and generates 3 personalized, context-aware insights based on the user's highest emitting category.

## 4. Engineering Assumptions
* **Grid Intensity:** Assumed a baseline global average of 0.475 kg CO2e/kWh for electricity.
* **Vehicle Emissions:** Utilized standard EPA baseline coefficients for transport vehicle archetypes (e.g., 0.170 kg/km for sedans).
* **Carpooling Logic:** Assumed a proportional distribution of transport emissions across all passengers to incentivize shared rides.

## 5. Local Setup & Testing
To run this project locally:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload