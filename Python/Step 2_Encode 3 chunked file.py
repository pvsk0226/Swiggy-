import pandas as pd
import glob
import os

# Input and output folders
in_dir = r"C:\Pavithra\Swiggy\chunks"
out_dir = r"C:\Pavithra\Swiggy\encoded_chunks"
os.makedirs(out_dir, exist_ok=True)

# Columns to one-hot encode
onehot_cols = ['name', 'city', 'cuisine']

# Get list of chunk files
chunk_files = sorted(glob.glob(os.path.join(in_dir, "swiggy_part_*.csv")))

print("Starting One-Hot Encoding for chunks...\n")

for i, file in enumerate(chunk_files, start=1):
    print(f"Processing {file}...")
    chunk = pd.read_csv(file, encoding='utf-8')

    # Keep only columns that exist
    available_cols = [col for col in onehot_cols if col in chunk.columns]

    # One-hot encode only those
    chunk_encoded = pd.get_dummies(chunk, columns=available_cols, drop_first=True)

    # Save encoded chunk
    out_path = os.path.join(out_dir, f"swiggy_onehot_part_{i:03d}.csv")
    chunk_encoded.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Saved encoded chunk  {out_path}\n")

print(" All chunks one-hot encoded successfully!")
