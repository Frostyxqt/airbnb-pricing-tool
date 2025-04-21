# pricing_tool.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Vacation Rental Pricing Tool", layout="centered")

st.title("🏡 AI Pricing Strategy Tool")
st.write("Enter your property details to get a smart pricing recommendation based on mock market data.")

# --- INPUT FORM ---
with st.form("property_form"):
    name = st.text_input("Property Name")
    location = st.text_input("Location (City or Neighborhood)", "Miami Beach")
    bedrooms = st.number_input("Bedrooms", 1, 10, 2)
    bathrooms = st.number_input("Bathrooms", 1, 10, 1)
    guests = st.number_input("Max Guests", 1, 20, 4)
    property_type = st.selectbox("Property Type", ["Apartment", "House", "Studio", "Condo"])
    amenities = st.multiselect(
        "Amenities",
        ["Wi-Fi", "Pool", "Hot Tub", "Kitchen", "Washer", "Parking", "AC", "Pet Friendly"],
    )
    base_cost = st.number_input("Operating Cost per Night (optional)", min_value=0.0, step=10.0)

    submitted = st.form_submit_button("Evaluate")

# --- MOCK MARKET DATA ---
def generate_mock_market_data(location):
    np.random.seed(hash(location) % 100000)  # for consistent results per location
    return pd.DataFrame({
        "price": np.random.normal(loc=180, scale=40, size=50).clip(60, 400),
        "bedrooms": np.random.choice([1, 2, 3, 4], size=50),
        "bathrooms": np.random.choice([1, 2, 3], size=50),
        "guests": np.random.choice([2, 4, 6, 8], size=50),
        "amenities_score": np.random.uniform(0.5, 1.0, size=50),
    })

# --- PRICING LOGIC ---
def calculate_pricing(prop, market_df):
    market_avg = market_df["price"].mean()

    size_score = (prop["bedrooms"] + 0.5 * prop["bathrooms"] + 0.25 * prop["guests"]) / 10
    amenity_score = len(prop["amenities"]) / 8  # out of 1
    score = 0.5 * size_score + 0.5 * amenity_score

    recommended_base = market_avg * (0.9 + score * 0.4)
    weekend_price = recommended_base * 1.15
    seasonal_boost = recommended_base * 1.2
    min_price = max(recommended_base * 0.8, prop["base_cost"])
    max_price = recommended_base * 1.5

    return {
        "base": round(recommended_base, 2),
        "weekend": round(weekend_price, 2),
        "seasonal": round(seasonal_boost, 2),
        "min": round(min_price, 2),
        "max": round(max_price, 2),
    }

# --- OUTPUT ---
if submitted:
    mock_market = generate_mock_market_data(location)

    prop_data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "guests": guests,
        "amenities": amenities,
        "base_cost": base_cost,
    }

    pricing = calculate_pricing(prop_data, mock_market)

    st.success("📈 Pricing Strategy Generated!")
    st.metric("🏷️ Recommended Base Price", f"${pricing['base']}")
    st.metric("📆 Weekend Price", f"${pricing['weekend']}")
    st.metric("☀️ Seasonal Price", f"${pricing['seasonal']}")
    st.metric("🔻 Minimum Price", f"${pricing['min']}")
    st.metric("🔺 Maximum Price", f"${pricing['max']}")

    st.markdown("---")
    st.subheader("📊 Market Snapshot (Mock Data)")
    st.bar_chart(mock_market["price"])

---

## 🚀 Run It
# Install Streamlit if you haven't:

```bash
pip install streamlit
