# step10_streamlit_app.py
import streamlit as st
import pandas as pd

# === PATHS ===
cosine_master_path = r"C:\Pavithra\Swiggy\cosine_master.pkl"
cleaned_data_path = r"C:\Pavithra\Swiggy\swiggy_cleaned.csv"  # updated path

# === LOAD DATA ===
@st.cache_data
def load_data():
    cleaned_data = pd.read_csv(cleaned_data_path)
    cosine_master = pd.read_pickle(cosine_master_path)
    return cleaned_data, cosine_master

cleaned_data, cosine_master = load_data()
restaurant_names = cleaned_data['name'].fillna("Unknown").tolist()

# === RECOMMENDATION FUNCTION ===
def get_recommendations_by_name(target_restaurant, top_n=5):
    if target_restaurant not in restaurant_names:
        return pd.DataFrame()
    
    target_index = restaurant_names.index(target_restaurant)
    scores = cosine_master.iloc[target_index].values
    similarities = list(enumerate(scores))
    
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in similarities[1:top_n+1]]
    
    recommendations = cleaned_data.iloc[top_indices][['name', 'city', 'cuisine', 'cost', 'rating']].copy()
    recommendations['cost'] = recommendations['cost'].astype(str).str.replace('₹','Rs.')
    return recommendations

# === STREAMLIT APP ===
st.title("🍽️ Swiggy Restaurant Recommendation System")

# Sidebar for user preferences
st.sidebar.header("User Preferences")
city = st.sidebar.text_input("City")
cuisine = st.sidebar.text_input("Cuisine")
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0)
max_price = st.sidebar.number_input("Maximum Price (Rs.)", min_value=0, value=10000)

# Filter data based on preferences
filtered_data = cleaned_data.copy()
if city:
    filtered_data = filtered_data[filtered_data['city'].str.contains(city, case=False, na=False)]
if cuisine:
    filtered_data = filtered_data[filtered_data['cuisine'].str.contains(cuisine, case=False, na=False)]
filtered_data = filtered_data[pd.to_numeric(filtered_data['rating'], errors='coerce').fillna(0) >= min_rating]
filtered_data = filtered_data[pd.to_numeric(filtered_data['cost'].str.replace('₹','').str.replace(',',''), errors='coerce').fillna(0) <= max_price]

# Show number of restaurants found
st.write(f"Found {len(filtered_data)} restaurants matching your preferences.")

# User selects a restaurant for similarity-based recommendation
target_restaurant = st.selectbox("Select a restaurant to find similar options:", filtered_data['name'].tolist())

if target_restaurant:
    recommendations = get_recommendations_by_name(target_restaurant, top_n=5)
    st.write(f"Top 5 recommendations similar to '{target_restaurant}':")
    st.dataframe(recommendations)
