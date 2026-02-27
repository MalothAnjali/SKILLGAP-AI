from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.match_resume_job import match_skills_function  # modify based on your function name

app = Flask(__name__)
CORS(app)  # allow frontend connection

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    
    resume_text = data.get("resume")
    job_text = data.get("job")

    matched, missing, percentage, courses = match_skills_function(resume_text, job_text)

    return jsonify({
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": percentage,
        "recommended_courses": courses
    })

if __name__ == "__main__":
    app.run(debug=True)