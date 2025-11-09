import pandas as pd
import glob
import pickle

# Path to your 15 encoded pickle chunks
chunk_paths = sorted(glob.glob(r"C:\Pavithra\Swiggy\swiggy_part_*.pkl"))

dfs = []
for path in chunk_paths:
    with open(path, "rb") as f:
        df = pickle.load(f)
    dfs.append(df)
    print(f"Loaded: {path}")

# Merge all chunks
final_df = pd.concat(dfs, ignore_index=True)

# Save as CSV
final_df.to_csv(r"C:\Pavithra\Swiggy\encoded_data.csv", index=False, encoding='utf-8')
print(" All chunks merged and saved as encoded_data.csv")
