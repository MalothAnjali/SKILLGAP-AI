import pandas as pd
from pymongo import MongoClient

# 1. Load CSV
csv_path = r"C:\Users\RAGAM LIKHITHA\SkillGap_AI\courses\coursera.csv"
df = pd.read_csv(csv_path)

# 2. Clean and preprocess
# Fill missing skills with empty string
df['skills'] = df['skills'].fillna("")

# Optional: split skills into list
df['skills'] = df['skills'].apply(lambda x: [skill.strip() for skill in x.split(",")] if x else [])

# 3. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SkillGap_AI"]
collection = db["courses"]  # New collection for courses

# 4. Convert dataframe to dictionary records
records = df.to_dict(orient='records')

# 5. Insert into MongoDB
collection.insert_many(records)

print(f"✅ Inserted {len(records)} courses into MongoDB")