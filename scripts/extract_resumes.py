import os
import pdfplumber
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["SkillGap_AI"]
collection = db["resumes"]

# Path to your data folder
base_path = r"C:\Users\RAGAM LIKHITHA\SkillGap_AI\data"

batch_size = 50
resume_batch = []
count = 0
max_resumes_to_add = 1000

# Get all filenames already in DB (lowercase for consistency)
existing_files = set(doc["filename"].lower() for doc in collection.find({}, {"filename": 1}))

# Loop through all PDFs in subfolders
for category_folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, category_folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            # check lowercase to avoid mismatch
            if filename.endswith(".pdf") and filename.lower() not in existing_files:
                file_path = os.path.join(folder_path, filename)
                text = ""
                try:
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                except Exception as e:
                    print(f"❌ Failed to process {filename}: {e}")
                    continue

                doc = {
                    "filename": filename,
                    "category": category_folder,
                    "text": text,
                    "skills": []
                }

                resume_batch.append(doc)
                count += 1

                if len(resume_batch) >= batch_size:
                    collection.insert_many(resume_batch)
                    resume_batch = []
                    print(f"Inserted {count} new resumes so far...")

                if count >= max_resumes_to_add:
                    break
        if count >= max_resumes_to_add:
            break

if resume_batch:
    collection.insert_many(resume_batch)

print(f"✅ Finished processing and inserting {count} new resumes into MongoDB!")
