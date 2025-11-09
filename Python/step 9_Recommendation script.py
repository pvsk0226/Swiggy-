import pandas as pd
import os
import sys

# Enable UTF-8 output to avoid chramap issues
sys.stdout.reconfigure(encoding='utf-8')

# === PATHS ===
cosine_master_path = r"C:\Pavithra\Swiggy\cosine_master.pkl"
cleaned_data_path = r"C:\Pavithra\Swiggy\swiggy_cleaned.csv"
output_folder = r"C:\Pavithra\Swiggy\recommendations"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# === LOAD MASTER COSINE SIMILARITY FILE ===
cosine_master = pd.read_pickle(cosine_master_path)
print(f"Loaded cosine master shape: {cosine_master.shape}")

# === LOAD CLEANED DATA ===
cleaned_data = pd.read_csv(cleaned_data_path, usecols=['id', 'name', 'city', 'cuisine', 'cost'])
restaurant_names = cleaned_data['name'].fillna("Unknown").tolist()
print(f"Loaded cleaned data with {len(cleaned_data)} restaurants")

# === FUNCTION TO GET RECOMMENDATIONS ===
def get_recommendations(target_restaurant, top_n=5, save_csv=True):
    """
    Return top N similar restaurants for a given restaurant name.
    """
    if target_restaurant not in restaurant_names:
        print(f" Restaurant '{target_restaurant}' not found.")
        return pd.DataFrame()
    
    target_index = restaurant_names.index(target_restaurant)
    scores = cosine_master.iloc[target_index].values
    similarities = list(enumerate(scores))
    
    # Sort by similarity (highest first) and skip self
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in similarities[1:top_n+1]]
    
    # Map indices to cleaned_data
    recommendations = cleaned_data.iloc[top_indices][['name', 'city', 'cuisine', 'cost']].copy()
    
    # Replace Rupee symbol for safe printing
    recommendations['cost'] = recommendations['cost'].astype(str).str.replace('₹', 'Rs.')
    
    print(f"\nTop {top_n} recommendations for '{target_restaurant}':\n")
    print(recommendations)
    
    # Save to CSV
    if save_csv:
        safe_name = target_restaurant.replace(" ", "_").replace("/", "_")
        output_file = os.path.join(output_folder, f"recommendations_{safe_name}.csv")
        recommendations.to_csv(output_file, index=False)
        print(f"\nRecommendations saved to: {output_file}")
    
    return recommendations

# === EXAMPLE USAGE ===
get_recommendations("Hotel Saravana Bhavan", top_n=5)
