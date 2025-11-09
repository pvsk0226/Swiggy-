import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Paths
encoded_path = r"C:\Pavithra\Swiggy\encoded_data.csv"
output_folder = r"C:\Pavithra\Swiggy\cosine_chunks"

os.makedirs(output_folder, exist_ok=True)

chunk_size = 3000
reader = pd.read_csv(encoded_path, chunksize=chunk_size)
chunk_index = 1

for chunk in reader:
    print(f"Processing chunk {chunk_index} with {len(chunk)} rows...")

    # Drop ID column if present
    chunk = chunk.drop(columns=['id'], errors='ignore')

    # 🧹 Step 1: Replace bad entries like '--' with NaN
    chunk = chunk.replace('--', np.nan)

    # 🧹 Step 2: Convert all data to numeric (non-convertible values → NaN)
    chunk = chunk.apply(pd.to_numeric, errors='coerce')

    # 🧹 Step 3: Fill missing values with 0
    chunk = chunk.fillna(0)

    #  Step 4: Compute cosine similarity
    cos_sim = cosine_similarity(chunk)

    # ✅ Step 5: Save the chunk's similarity matrix
    cos_df = pd.DataFrame(cos_sim)
    cos_df.to_csv(f"{output_folder}\\cosine_chunk_{chunk_index}.csv", index=False)

    print(f" Saved cosine_chunk_{chunk_index}.csv successfully!\n")
    chunk_index += 1

print(" All cosine similarity chunks processed and saved successfully!")
