from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["SkillGap_AI"]

resume_collection = db["resumes"]
job_collection = db["job_skills"]

def calculate_match(resume_skills, job_skills):
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set

    if len(job_set) == 0:
        match_percent = 0
    else:
        match_percent = (len(matched) / len(job_set)) * 100

    return list(matched), list(missing), round(match_percent, 2)


resume = resume_collection.find_one()
job = job_collection.find_one()

resume_skills = resume.get("skills", [])
job_skills_text = job.get("job_skills", "")

job_skills = [s.strip() for s in job_skills_text.split(",")]

print("Resume Skills:", resume_skills)
print("Job Skills:", job_skills)

matched, missing, percent = calculate_match(resume_skills, job_skills)

print("Matched Skills:", matched)
print("Missing Skills:", missing)
print("Match Percentage:", percent, "%")