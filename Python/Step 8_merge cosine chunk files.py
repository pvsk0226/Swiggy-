import os
import pandas as pd

# === PATH TO COSINE CHUNK FOLDER ===
chunk_folder = r"C:\Pavithra\Swiggy\cosine_chunks"
output_pickle = r"C:\Pavithra\Swiggy\cosine_master.pkl"

# === LIST ALL CSV CHUNK FILES ===
chunk_files = sorted([f for f in os.listdir(chunk_folder)
                      if f.lower().startswith("cosine_chunk_") and f.lower().endswith(".csv")])

print(f"Found {len(chunk_files)} chunk files.")

if not chunk_files:
    print("No chunk files found. Check folder path or filenames.")
else:
    # === LOAD AND MERGE CHUNKS ===
    chunks = []
    for file in chunk_files:
        file_path = os.path.join(chunk_folder, file)
        print(f"Loading {file}...")
        df_chunk = pd.read_csv(file_path, header=None)  # cosine files usually have no header
        chunks.append(df_chunk)

    # Concatenate all chunks
    cosine_master = pd.concat(chunks, axis=0, ignore_index=True)
    print(f"Merged cosine similarity shape: {cosine_master.shape}")

    # Save as Pickle for faster access
    cosine_master.to_pickle(output_pickle)
    print(f" Master Pickle saved: {output_pickle}")
