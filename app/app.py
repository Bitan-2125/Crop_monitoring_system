
# Importing essential libraries and modules

from flask import Flask, render_template, request, jsonify, Response
from markupsafe import Markup
import numpy as np
import pandas as pd
from utils.disease import disease_dic
from utils.fertilizer import fertilizer_dic
import requests
import config
import pickle
import io
import base64
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9
from groq import Groq
import markdown
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tavily import TavilyClient
# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()


# Loading crop recommendation model

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


# =========================================================================================

# Custom functions for calculations


def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    try:
        api_key = config.weather_api_key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url, timeout=5)
        x = response.json()

        if "main" in x:
            temperature = round((x["main"]["temp"] - 273.15), 2)
            humidity = x["main"]["humidity"]
            return temperature, humidity
        else:
            app.logger.warning(f"Weather API error for city '{city_name}': {x}")
            return None
    except Exception as e:
        app.logger.error(f"Weather fetch failed: {e}")
        return None


def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string), confidence (float)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Convert logits to probabilities
    probs = torch.nn.functional.softmax(yb, dim=1)
    # Pick index with highest probability
    confidence, preds = torch.max(probs, dim=1)
    prediction = disease_classes[preds[0].item()]
    confidence_pct = round(confidence[0].item() * 100, 2)
    return prediction, confidence_pct

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


def get_crop_tips(crop_name):
    """Use Groq LLM to get best practices for growing the recommended crop."""
    try:
        client = Groq(api_key=config.groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Give me 5 concise best practices for growing {crop_name} successfully. "
                        "Format as a numbered list. Keep each point to 1-2 sentences. "
                        "Focus on soil preparation, watering, fertilization, pest control, and harvesting tips."
                    ),
                }
            ],
            model="openai/gpt-oss-120b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return None


def translate_to_hindi(text):
    """Translate given plain text to Hindi using Groq llama-3.3-70b-versatile."""
    try:
        client = Groq(api_key=config.groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Translate the following text to Hindi. "
                        "Keep the same formatting (numbered lists, bold etc). "
                        "Return only the translated text, nothing else.\n\n"
                        + text
                    ),
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        result = chat_completion.choices[0].message.content
        return Markup(markdown.markdown(result))
    except Exception as e:
        return None


def tavily_search(query, topic="general", max_results=5, include_images=True):
    """Run a Tavily search and return results + image URLs."""
    try:
        client = TavilyClient(api_key=config.tavily_api_key)
        response = client.search(
            query=query,
            topic=topic,
            max_results=max_results,
            include_images=include_images,
            include_answer=True,
            search_depth="advanced",
        )
        return response
    except Exception as e:
        return None


def groq_vision_describe(image_url, prompt):
    """Use Groq vision model to describe/analyze an image from URL."""
    try:
        client = Groq(api_key=config.groq_api_key)
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_completion_tokens=512,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None


def make_cost_revenue_chart(cost, revenue, crop_name):
    """Generate a bar chart comparing estimated cost vs revenue. Returns base64 PNG."""
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(['Input Cost', 'Expected Revenue'], [cost, revenue],
                  color=['#f4a261', '#52b788'], width=0.45, edgecolor='white', linewidth=1.2)
    ax.set_title(f'Cost vs Revenue — {crop_name}', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylabel('Amount (₹)', fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{int(x):,}'))
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(cost, revenue) * 0.02,
                f'₹{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_facecolor('#f8fdf9')
    fig.patch.set_facecolor('#ffffff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def make_monthly_calendar_chart(season):
    """Generate a Gantt-style monthly activity chart. Returns base64 PNG."""
    season_map = {
        'Kharif': {
            'Land Prep': (6, 1), 'Sowing': (7, 1), 'Fertilizing': (7, 2),
            'Irrigation': (8, 2), 'Pest Control': (8, 2), 'Harvesting': (10, 1),
        },
        'Rabi': {
            'Land Prep': (10, 1), 'Sowing': (11, 1), 'Fertilizing': (11, 2),
            'Irrigation': (12, 2), 'Pest Control': (1, 2), 'Harvesting': (3, 1),
        },
        'Zaid': {
            'Land Prep': (3, 1), 'Sowing': (3, 1), 'Fertilizing': (4, 1),
            'Irrigation': (4, 2), 'Pest Control': (5, 1), 'Harvesting': (6, 1),
        },
    }
    key = next((k for k in season_map if k in season), 'Kharif')
    activities = season_map[key]
    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    colors = ['#52b788','#f4a261','#2d6a4f','#74c69d','#d8f3dc','#b7e4c7']

    fig, ax = plt.subplots(figsize=(8, 3.5))
    for i, (activity, (start_month, duration)) in enumerate(activities.items()):
        # convert month to 0-indexed offset
        start = (start_month - 1) % 12
        ax.barh(i, duration, left=start, color=colors[i % len(colors)],
                edgecolor='white', linewidth=1, height=0.6)
        ax.text(start + duration / 2, i, activity, ha='center', va='center',
                fontsize=8, fontweight='bold', color='#1b1b2f')

    ax.set_yticks(range(len(activities)))
    ax.set_yticklabels(list(activities.keys()), fontsize=8)
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.set_title(f'Monthly Activity Calendar — {key} Season', fontsize=10, fontweight='bold', pad=8)
    ax.set_facecolor('#f8fdf9')
    fig.patch.set_facecolor('#ffffff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
app = Flask(__name__)


@app.route('/translate-hindi', methods=['POST'])
def translate_hindi():
    from flask import jsonify
    blocks = request.json.get('blocks', [])
    if not blocks:
        return jsonify({'error': 'No text provided'}), 400
    try:
        client = Groq(api_key=config.groq_api_key)
        translated = []
        for text in blocks:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Translate the following text to Hindi. "
                            "Keep the same formatting (numbered lists, bold etc). "
                            "Return only the translated text, nothing else.\n\n"
                            + text
                        ),
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            result = chat_completion.choices[0].message.content
            translated.append(str(Markup(markdown.markdown(result))))
        return jsonify({'blocks': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# render home page


@ app.route('/')
def home():
    title = 'Harvestify - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Harvestify - Crop Recommendation'
    return render_template('crop.html', title=title)

# render fertilizer recommendation form page


@ app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'Harvestify - Fertilizer Suggestion'

    return render_template('fertilizer.html', title=title)

# render disease prediction input page




# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Harvestify - Crop Recommendation'

    if request.method == 'POST':
        try:
            N = int(request.form['nitrogen'])
            P = int(request.form['phosphorous'])
            K = int(request.form['pottasium'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
            city = request.form.get("city", "").strip()

            weather = weather_fetch(city)
            if weather is not None:
                temperature, humidity = weather
                data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
                my_prediction = crop_recommendation_model.predict(data)
                final_prediction = my_prediction[0]
                tips = get_crop_tips(final_prediction)
                if tips:
                    tips = Markup(markdown.markdown(tips))
                return render_template('crop-result.html', prediction=final_prediction, tips=tips, title=title)
            else:
                return render_template('try_again.html', title=title)
        except Exception as e:
            app.logger.error(f"Crop prediction error: {e}")
            return render_template('try_again.html', title=title)

# render fertilizer recommendation result page


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'Harvestify - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer-result.html', recommendation=response, title=title)

# render disease prediction result page


@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Harvestify - Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', title=title)
        try:
            img = file.read()

            prediction, confidence = predict_image(img)

            prediction = Markup(str(disease_dic[prediction]))
            return render_template('disease-result.html', prediction=prediction, confidence=confidence, title=title)
        except:
            pass
    return render_template('disease.html', title=title)


# ===============================================================================================
# MARKET PRICE INSIGHT

@app.route('/market-price')
def market_price():
    title = 'Harvestify - Market Price Insight'
    return render_template('market-price.html', title=title)


@app.route('/market-price-result', methods=['POST'])
def market_price_result():
    title = 'Harvestify - Market Price Insight'
    crop = request.form.get('crop', '').strip()
    state = request.form.get('state', '').strip()
    season = request.form.get('season', '').strip()

    if not crop:
        return render_template('try_again.html', title=title)

    try:
        # 1. Tavily search for real market data
        search_query = f"{crop} market price India {state} {season} mandi 2024 2025"
        tavily_data = tavily_search(search_query, topic="general", max_results=4, include_images=True)
        search_context = ""
        search_sources = []
        search_images = []
        if tavily_data:
            if tavily_data.get('answer'):
                search_context = f"Recent web data: {tavily_data['answer']}\n\n"
            for r in tavily_data.get('results', []):
                search_context += f"- {r.get('title','')}: {r.get('content','')[:300]}\n"
                search_sources.append({'title': r.get('title',''), 'url': r.get('url','')})
            search_images = tavily_data.get('images', [])[:3]

        # 2. Groq LLM for structured insight (grounded with Tavily context)
        client = Groq(api_key=config.groq_api_key)
        prompt = (
            f"You are an agricultural market expert for India. "
            f"Using the following real-time web data as context:\n{search_context}\n"
            f"Provide a market price insight report for {crop} in {state if state else 'India'} "
            f"during {season if season else 'the current season'}.\n\n"
            "Include:\n"
            "1. Typical price range (₹ per quintal or kg)\n"
            "2. Best months to sell for maximum profit\n"
            "3. Key market factors affecting price\n"
            "4. Top 3 mandis/markets to sell in this region\n"
            "5. Price trend outlook (rising/stable/falling) with reason\n\n"
            "Format as a numbered list with clear headings. Be specific with numbers."
        )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        result = chat_completion.choices[0].message.content
        insight = Markup(markdown.markdown(result))

        # 3. Groq vision: describe first relevant image if available
        vision_caption = None
        vision_image_url = None
        if search_images:
            img_url = search_images[0] if isinstance(search_images[0], str) else search_images[0].get('url','')
            if img_url:
                vision_image_url = img_url
                vision_caption = groq_vision_describe(
                    img_url,
                    f"This image is related to {crop} farming or market in India. "
                    "Briefly describe what you see in 1-2 sentences, focusing on agricultural relevance."
                )

        return render_template('market-price-result.html', crop=crop, state=state,
                               season=season, insight=insight, sources=search_sources,
                               vision_image_url=vision_image_url, vision_caption=vision_caption,
                               title=title)
    except Exception as e:
        app.logger.error(f"Market price error: {e}")
        return render_template('try_again.html', title=title)


# ===============================================================================================
# SMART CROP PLANNING

@app.route('/crop-planning')
def crop_planning():
    title = 'Harvestify - Smart Crop Planning'
    return render_template('crop-planning.html', title=title)


@app.route('/crop-planning-result', methods=['POST'])
def crop_planning_result():
    title = 'Harvestify - Smart Crop Planning'
    land_size = request.form.get('land_size', '').strip()
    land_unit = request.form.get('land_unit', 'acres')
    budget = request.form.get('budget', '').strip()
    state = request.form.get('state', '').strip()
    season = request.form.get('season', '').strip()
    soil_type = request.form.get('soil_type', '').strip()
    water_source = request.form.get('water_source', '').strip()

    if not land_size or not season:
        return render_template('try_again.html', title=title)

    try:
        # 1. Tavily search for regional crop data
        search_query = f"best crops to grow {state if state else 'India'} {season} {soil_type} soil farming 2025"
        tavily_data = tavily_search(search_query, topic="general", max_results=4, include_images=True)
        search_context = ""
        search_sources = []
        search_images = []
        if tavily_data:
            if tavily_data.get('answer'):
                search_context = f"Recent web data: {tavily_data['answer']}\n\n"
            for r in tavily_data.get('results', []):
                search_context += f"- {r.get('title','')}: {r.get('content','')[:300]}\n"
                search_sources.append({'title': r.get('title',''), 'url': r.get('url','')})
            search_images = tavily_data.get('images', [])[:3]

        # 2. Groq LLM for the full plan
        client = Groq(api_key=config.groq_api_key)
        prompt = (
            f"You are an expert agricultural planner for India. "
            f"Using the following real-time web data as context:\n{search_context}\n"
            f"Create a smart crop plan for a farmer with the following details:\n"
            f"- Land: {land_size} {land_unit}\n"
            f"- Budget: ₹{budget if budget else 'moderate'}\n"
            f"- Location: {state if state else 'India'}\n"
            f"- Season: {season}\n"
            f"- Soil type: {soil_type if soil_type else 'not specified'}\n"
            f"- Water source: {water_source if water_source else 'not specified'}\n\n"
            "Provide:\n"
            "1. Recommended primary crop with justification\n"
            "2. Intercrop or secondary crop suggestion\n"
            "3. Month-by-month activity calendar (sowing to harvest)\n"
            "4. Estimated input cost (₹) and expected revenue (₹) — give specific numbers\n"
            "5. Crop rotation advice for next season\n"
            "6. Key risks and mitigation tips\n\n"
            "IMPORTANT: In section 4, always include two lines formatted exactly like:\n"
            "ESTIMATED_COST: <number>\n"
            "ESTIMATED_REVENUE: <number>\n"
            "Format the rest clearly with numbered sections and sub-points."
        )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        raw_plan = chat_completion.choices[0].message.content

        # 3. Extract cost/revenue for chart
        import re
        cost_match = re.search(r'ESTIMATED_COST:\s*([\d,]+)', raw_plan)
        revenue_match = re.search(r'ESTIMATED_REVENUE:\s*([\d,]+)', raw_plan)
        cost_val = int(cost_match.group(1).replace(',', '')) if cost_match else int(budget or 50000)
        revenue_val = int(revenue_match.group(1).replace(',', '')) if revenue_match else int(cost_val * 1.6)
        # Strip the machine-readable lines from display
        display_plan = re.sub(r'ESTIMATED_(COST|REVENUE):\s*[\d,]+\n?', '', raw_plan)
        plan = Markup(markdown.markdown(display_plan))

        # 4. Generate charts
        primary_crop_match = re.search(r'(?:primary crop|recommend)[^\n]*?(\w+)', raw_plan, re.IGNORECASE)
        crop_name = primary_crop_match.group(1) if primary_crop_match else "Crop"
        chart_cost_revenue = make_cost_revenue_chart(cost_val, revenue_val, crop_name)
        chart_calendar = make_monthly_calendar_chart(season)

        # 5. Groq vision on first search image
        vision_caption = None
        vision_image_url = None
        if search_images:
            img_url = search_images[0] if isinstance(search_images[0], str) else search_images[0].get('url','')
            if img_url:
                vision_image_url = img_url
                vision_caption = groq_vision_describe(
                    img_url,
                    f"This image is related to farming in {state if state else 'India'} during {season}. "
                    "Briefly describe what you see in 1-2 sentences, focusing on agricultural relevance."
                )

        return render_template('crop-planning-result.html', plan=plan, land_size=land_size,
                               land_unit=land_unit, state=state, season=season,
                               chart_cost_revenue=chart_cost_revenue,
                               chart_calendar=chart_calendar,
                               sources=search_sources,
                               vision_image_url=vision_image_url,
                               vision_caption=vision_caption,
                               title=title)
    except Exception as e:
        app.logger.error(f"Crop planning error: {e}")
        return render_template('try_again.html', title=title)


@app.route('/crop-planning-pdf', methods=['POST'])
def crop_planning_pdf():
    """Render the crop plan as a downloadable PDF using xhtml2pdf."""
    try:
        from xhtml2pdf import pisa
        plan_html = request.form.get('plan_html', '')
        chart_cost_revenue = request.form.get('chart_cost_revenue', '')
        chart_calendar = request.form.get('chart_calendar', '')
        land_size = request.form.get('land_size', '')
        land_unit = request.form.get('land_unit', '')
        state = request.form.get('state', '')
        season = request.form.get('season', '')

        chart_cal_tag = f'<img src="data:image/png;base64,{chart_calendar}" style="width:100%;"/>' if chart_calendar else ''
        chart_cr_tag = f'<img src="data:image/png;base64,{chart_cost_revenue}" style="width:60%;"/>' if chart_cost_revenue else ''

        pdf_html = f"""<!DOCTYPE html><html><head>
        <meta charset="utf-8">
        <style>
          @page {{ margin: 2cm; }}
          body {{ font-family: Helvetica, Arial, sans-serif; color: #2d3436; line-height: 1.6; font-size: 11pt; }}
          h1 {{ color: #2d6a4f; font-size: 16pt; border-bottom: 1px solid #52b788; padding-bottom: 4pt; }}
          h2, h3, h4 {{ color: #2d6a4f; }}
          .meta {{ color: #636e72; font-size: 9pt; margin-bottom: 12pt; }}
          img {{ max-width: 100%; margin: 8pt 0; }}
          ul, ol {{ padding-left: 16pt; }}
          li {{ margin-bottom: 3pt; }}
          .footer {{ margin-top: 16pt; font-size: 8pt; color: #636e72; border-top: 1px solid #e0e0e0; padding-top: 4pt; }}
        </style></head><body>
        <h1>Smart Crop Plan - Harvestify</h1>
        <div class="meta">{land_size} {land_unit} | {state} | {season}</div>
        {chart_cal_tag}
        {chart_cr_tag}
        {plan_html}
        <div class="footer">Generated by Harvestify | AI-powered agricultural planning</div>
        </body></html>"""

        pdf_buf = io.BytesIO()
        pisa_status = pisa.CreatePDF(pdf_html, dest=pdf_buf)
        if pisa_status.err:
            raise Exception(f"pisa error: {pisa_status.err}")
        pdf_buf.seek(0)
        return Response(
            pdf_buf.read(),
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment; filename=crop_plan.pdf'}
        )
    except Exception as e:
        app.logger.error(f"PDF generation error: {e}")
        return f"PDF generation failed: {str(e)}", 500


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)
