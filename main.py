import pandas as pd

# Replace 'your_file.parquet' with the path to your snappy.parquet file
df = pd.read_parquet('part-00000-9230b837-b1e0-4254-8b88-ed2976e9cee9-c000.snappy.parquet', engine='pyarrow') 
# or use engine='fastparquet' if you prefer

print(df.head())
