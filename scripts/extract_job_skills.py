from pymongo import MongoClient
from skills_master_list import MASTER_SKILLS
client = MongoClient("mongodb://localhost:27017/")
db = client["SkillGap_AI"]

job_collection = db["job_summary"]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in MASTER_SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


for job in job_collection.find({"skills_extracted": {"$ne": True}}):
    job_id = job["_id"]
    summary = job.get("job_summary", "")

    skills = extract_skills(summary)

    job_collection.update_one(
        {"_id": job_id},
        {
            "$set": {
                "extracted_skills": skills,
                "skills_extracted": True
            }
        }
    )

print("✅ Job skill extraction completed")