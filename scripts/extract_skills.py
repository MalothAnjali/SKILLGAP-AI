from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["SkillGap_AI"]
collection = db["resumes"]

# Your skills dictionary (expand as needed)
skills_dict = ["Python", "SQL", "Excel", "PowerPoint", "JavaScript", "React", "Accounting", "Finance"]

batch_size = 50
processed = 0

for doc in collection.find():
    text = doc["text"].lower()
    found_skills = [skill for skill in skills_dict if skill.lower() in text]
    
    if found_skills:
        collection.update_one({"_id": doc["_id"]}, {"$set": {"skills": found_skills}})
    
    processed += 1
    if processed % batch_size == 0:
        print(f"Processed skills for {processed} resumes...")

print(f"✅ Skill extraction completed for {processed} resumes")