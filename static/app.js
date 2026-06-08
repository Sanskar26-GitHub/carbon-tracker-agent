document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('carbon-form');
    const resultsSection = document.getElementById('results-section');
    const errorMsg = document.getElementById('error-message');

    // Result elements
    const transportOut = document.getElementById('transport-out');
    const utilityOut = document.getElementById('utility-out');
    const dietOut = document.getElementById('diet-out');
    const totalOut = document.getElementById('total-out');
    const insightsList = document.getElementById('insights-list');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Basic frontend validation
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Hide errors and results while loading
        errorMsg.hidden = true;

        // Gather payload
        const formData = new FormData(form);
        const payload = {
            transport_distance_km: parseFloat(formData.get('transport_distance_km')),
            vehicle_type: formData.get('vehicle_type'),
            carpool_passengers: parseInt(formData.get('carpool_passengers'), 10),
            electricity_kwh: parseFloat(formData.get('electricity_kwh')),
            natural_gas_m3: parseFloat(formData.get('natural_gas_m3')),
            diet_profile: formData.get('diet_profile')
        };

        try {
            const response = await fetch('/api/v1/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail ? JSON.stringify(errData.detail) : 'Failed to calculate footprint.');
            }

            const data = await response.json();

            // Populate results
            transportOut.textContent = data.transport_emissions.toFixed(2);
            utilityOut.textContent = data.utility_emissions.toFixed(2);
            dietOut.textContent = data.diet_emissions.toFixed(2);
            totalOut.textContent = data.total_emissions.toFixed(2);

            // Populate insights
            insightsList.innerHTML = ''; // Clear previous
            data.insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight; // Prevents XSS natively
                insightsList.appendChild(li);
            });

            // Show results section
            resultsSection.hidden = false;

            // Scroll to results on mobile
            if (window.innerWidth < 900) {
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }

        } catch (error) {
            console.error('API Error:', error);
            errorMsg.textContent = error.message || 'An unexpected error occurred.';
            errorMsg.hidden = false;
            resultsSection.hidden = true;
        }
    });
});
