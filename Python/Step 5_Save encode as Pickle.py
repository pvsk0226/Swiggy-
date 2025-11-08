import pandas as pd

# Path to your merged CSV file
merged_file = r"C:\Pavithra\Swiggy\swiggy_merged.csv"

# Path to save Pickle file
pickle_file = r"C:\Pavithra\Swiggy\swiggy_final.pkl"

# Load the merged CSV in chunks (memory safe)
chunks = pd.read_csv(merged_file, chunksize=50000, encoding="utf-8")

# Append chunks together in an efficient way
df_list = []
for chunk in chunks:
    df_list.append(chunk)

df_final = pd.concat(df_list, ignore_index=True)

# Save to Pickle
df_final.to_pickle(pickle_file)

print(f" Final encoded dataset saved successfully as Pickle:\n{pickle_file}")
