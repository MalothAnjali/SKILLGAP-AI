from pymongo import MongoClient

# Example data (replace this with your actual extracted resumes)
resume_texts = [
    {
        "filename": "John_Doe.pdf",
        "category": "Data_Science",
        "text": "John Doe is skilled in Python, SQL...",
        "skills": []
    },
    {
        "filename": "Jane_Smith.pdf",
        "category": "Web_Dev",
        "text": "Jane Smith knows JavaScript, React...",
        "skills": []
    }
]

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create/use database
db = client["SkillGap_AI"]

# Create/use collection
collection = db["resumes"]

# Insert documents
collection.insert_many(resume_texts)

print("✅ Resumes inserted into MongoDB")