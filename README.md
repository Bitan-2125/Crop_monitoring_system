# Harvestify 🌿

An AI-powered precision farming web application that helps farmers make smarter decisions — from choosing the right crop to detecting plant diseases and planning an entire season.

---

## Features

### 1. Crop Recommendation
Enter your soil's NPK (Nitrogen, Phosphorous, Potassium) values, pH, and rainfall along with your city name. Harvestify fetches live temperature and humidity from OpenWeather and runs a trained Random Forest model to recommend the most suitable crop for your conditions. An LLM then generates 5 tailored growing tips for that crop.

### 2. Fertilizer Suggestion
Input your current soil nutrient levels and the crop you intend to grow. The system compares your values against ideal nutrient ratios and identifies whether your soil has an excess or deficiency of N, P, or K — then recommends the appropriate corrective fertilizer.

### 3. Plant Disease Detection
Upload a photo of a plant leaf. A custom ResNet9 deep learning model (trained on 38 disease classes) classifies the disease and returns:
- The crop type and disease name
- Cause of the disease
- Prevention and treatment steps
- Model confidence percentage shown as a color-coded progress bar

Supported crops: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.

### 4. Market Price Insight
Enter a crop name, state, and season. The system uses Tavily Search to pull real-time mandi and market data from the web, then uses a Groq LLM (Llama-3.3-70b) to generate a structured report covering:
- Current price range (₹ per quintal/kg)
- Best months to sell
- Key price-influencing factors
- Top 3 mandis/markets in the region
- Price trend outlook (rising/stable/falling)

A Groq vision model also describes any relevant image found during the search.

### 5. Smart Crop Planning
Provide your land size, budget, state, season, soil type, and water source. The system searches for region-specific farming data via Tavily, then generates a full season plan using Groq LLM including:
- Primary and intercrop recommendations
- Month-by-month activity calendar (Gantt chart)
- Estimated input cost vs expected revenue (bar chart)
- Crop rotation advice for the next season
- Key risks and mitigation tips

The full plan can be exported as a PDF.

### 6. Hindi Translation
On any result page, click "हिंदी में देखें" to translate the entire output to Hindi using the Groq Llama-3.3-70b model — making the app accessible to regional language users.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Bootstrap, JavaScript, Jinja2 |
| Backend | Python, Flask |
| Local ML | PyTorch (ResNet9), Scikit-Learn (Random Forest), NumPy, Pandas, Pillow |
| Generative AI | Groq API — Llama-3.3-70b (text), Llama-4-Scout (vision) |
| Web Search | Tavily Search API (Web-RAG) |
| Weather | OpenWeather API |
| Charts & PDF | Matplotlib, xhtml2pdf |

---

## Setup & Running Locally

**Prerequisites:** Python 3.8+, pip

1. Clone the repository
   ```
   git clone https://github.com/Gladiator07/Harvestify.git
   cd Harvestify/app
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file inside the `app/` directory (use `.env.example` as reference)
   ```
   WEATHER_API_KEY=your_openweather_key
   GROQ_API_KEY=your_groq_key
   TAVILY_API_KEY=your_tavily_key
   ```

4. Run the app
   ```
   python app.py
   ```

5. Open `http://localhost:5000` in your browser.

---

## Data Sources

- [Crop Recommendation Dataset](https://www.kaggle.com/atharvaingle/crop-recommendation-dataset)
- [Fertilizer Suggestion Dataset](https://github.com/Gladiator07/Harvestify/blob/master/Data-processed/fertilizer.csv)
- [Plant Disease Detection Dataset](https://www.kaggle.com/vipoooool/new-plant-diseases-dataset)

---

## Disclaimer

This is a research/proof-of-concept project. Do not use it as the sole basis for real farming decisions. The creator is not responsible for any outcomes resulting from its use.

---

## License

Licensed under the [GNU General Public License](./LICENSE).
