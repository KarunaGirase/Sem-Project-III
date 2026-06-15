async function predict() { 
  const data = {
    Villages: document.getElementById('Villages').value,
    Year: parseInt(document.getElementById('Year').value),
    Avg_Temp_C: parseFloat(document.getElementById('Avg_Temp_C').value),
    Avg_Humidity_Percent: parseFloat(document.getElementById('Avg_Humidity_Percent').value),
    Soil_Type: document.getElementById('Soil_Type').value,
    Soil_pH: parseFloat(document.getElementById('Soil_pH').value),
    Crop_Season: document.getElementById('Crop_Season').value,
    Soil_N_kg_ha: parseFloat(document.getElementById('Soil_N_kg_ha').value),
    Soil_P_kg_ha: parseFloat(document.getElementById('Soil_P_kg_ha').value),
    Soil_K_kg_ha: parseFloat(document.getElementById('Soil_K_kg_ha').value),
    Rainfall_mm: parseFloat(document.getElementById('Rainfall_mm').value),
    Farm_Area_ha: parseFloat(document.getElementById('Farm_Area_ha').value),
    Yield_kg_ha: 0.0,
    Fertilizer_Type: 'UNK',
    Fertilizer_Quantity_kg_ha: 0.0
  };

  try {
    const resp = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!resp.ok) {
      throw new Error('Server error ' + resp.status);
    }

    const res = await resp.json();
    const rd = document.getElementById('result');
    rd.style.display = 'block';

    // ✅ Match keys exactly with Flask’s response
    rd.innerHTML = `
      <h5 class="text-success">🌾 Prediction Results</h5>
      <p><strong>Crop Name:</strong> ${res["Predicted Crop"] || "N/A"}</p>
      <p><strong>Predicted Yield:</strong> ${res["Predicted Yield (kg/ha)"] ? res["Predicted Yield (kg/ha)"].toFixed(2) + " kg/ha" : "N/A"}</p>
      <p><strong>Fertilizer Type:</strong> ${res["Recommended Fertilizer"] || "N/A"}</p>
      <p><strong>Fertilizer Quantity:</strong> ${res["Fertilizer Quantity (kg/ha)"] ? res["Fertilizer Quantity (kg/ha)"].toFixed(2) + " kg/ha" : "N/A"}</p>`;
  } catch (e) {
    alert('Prediction failed: ' + e);
    console.error(e);
  }
}
