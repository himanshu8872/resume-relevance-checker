# main.py - UPGRADED VERSION
# In main.py, add this helper function near the top
import re

# In main.py, replace the old parse_analysis function with this one

def parse_analysis(analysis_text):
    score = 0.0
    verdict = "Not Found"
    try:
        # CORRECTED REGEX: Looks for asterisks around the label
        score_match = re.search(r"\*\*Relevance Score:\*\*\s*(\d{1,3})%", analysis_text)
        if score_match:
            score = float(score_match.group(1))

        # CORRECTED REGEX: Looks for asterisks around the label
        verdict_match = re.search(r"\*\*Verdict:\*\*\s*(High Suitability|Medium Suitability|Low Suitability)", analysis_text)
        if verdict_match:
            verdict = verdict_match.group(1)
    except Exception as e:
        print(f"Error parsing analysis text: {e}")

    return score, verdict

import os
import sqlite3
from flask import Flask, request, jsonify

from app.parser import parse_resume
from app.analyzer import get_gemini_response
from database import init_db

app = Flask(__name__)
DB_NAME = 'hackathon.db'

# Initialize the database
init_db()

@app.route('/jobs', methods=['POST', 'GET'])
def handle_jobs():
    """
    Handles GET requests to list all jobs and POST requests to add a new job.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO jobs (title, company, description_text) VALUES (?, ?, ?)",
            (data['title'], data['company'], data['description_text'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Job added successfully"}), 201
    else: # GET request
        cursor.execute("SELECT id, title, company FROM jobs")
        jobs = [{"id": row[0], "title": row[1], "company": row[2]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(jobs)

@app.route('/resumes', methods=['POST', 'GET'])
def handle_resumes():
    """
    Handles GET to list resumes and POST to add a new resume.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO resumes (candidate_name, email, text_content) VALUES (?, ?, ?)",
            (data['candidate_name'], data['email'], data['text_content'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Resume added successfully"}), 201
    else: # GET request
        cursor.execute("SELECT id, candidate_name, email FROM resumes")
        resumes = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(resumes)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Receives a job and resume ID, runs the AI analysis, and saves the result.
    """
    data = request.json
    job_id = data['job_id']
    resume_id = data['resume_id']

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT description_text FROM jobs WHERE id = ?", (job_id,))
    job_text = cursor.fetchone()[0]

    cursor.execute("SELECT text_content FROM resumes WHERE id = ?", (resume_id,))
    resume_text = cursor.fetchone()[0]
    
    analysis = get_gemini_response(resume_text, job_text)
    
    score, verdict = parse_analysis(analysis)
    
    cursor.execute(
        "INSERT INTO evaluations (resume_id, job_id, score, verdict, analysis_text) VALUES (?, ?, ?, ?, ?)",
        (resume_id, job_id, score, verdict, analysis)
    )

    conn.commit()
    cursor.execute("SELECT id FROM evaluations ORDER BY id DESC LIMIT 1")
    eval_id = cursor.fetchone()[0]
    conn.close()

    return jsonify({"evaluation_id": eval_id, "analysis": analysis})

@app.route('/evaluations/<int:eval_id>', methods=['GET'])
def get_evaluation(eval_id):
    """
    Fetches a ranked list of all evaluations for a specific job ID.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT analysis_text FROM evaluations WHERE id = ?", (eval_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({"analysis": result[0]})
    return jsonify({"error": "Evaluation not found"}), 404

@app.route('/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    job_count = cursor.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    resume_count = cursor.execute("SELECT COUNT(*) FROM resumes").fetchone()[0]
    evaluation_count = cursor.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
    avg_score = cursor.execute("SELECT AVG(score) FROM evaluations").fetchone()[0]

    conn.close()

    return jsonify({
        "total_jobs": job_count,
        "total_resumes": resume_count,
        "total_evaluations": evaluation_count,
        "average_score": avg_score if avg_score else 0
    })

@app.route('/evaluations/job/<int:job_id>', methods=['GET'])
def get_evaluations_for_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # This SQL query joins the tables to get the candidate's name and their score for a specific job,
    # then orders them from highest to lowest score.
    query = """
    SELECT
        r.candidate_name,
        r.email,
        e.score,
        e.verdict
    FROM evaluations e
    JOIN resumes r ON e.resume_id = r.id
    WHERE e.job_id = ?
    ORDER BY e.score DESC
    """

    cursor.execute(query, (job_id,))

    ranked_candidates = [
        {
            "candidate_name": row[0],
            "email": row[1],
            "score": f"{row[2]:.1f}%", # Format score as percentage string
            "verdict": row[3]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(ranked_candidates)


# --- DELETE Endpoints ---
"""Deletes a specific job and its related evaluations from the database."""
@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON") # This is needed to enforce cascade deletes
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Job deleted successfully"}), 200

@app.route('/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Resume deleted successfully"}), 200

@app.route('/evaluations/job/<int:job_id>/resume/<int:resume_id>', methods=['DELETE'])
def delete_evaluation(job_id, resume_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM evaluations WHERE job_id = ? AND resume_id = ?", (job_id, resume_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Evaluation deleted successfully"}), 200       


if __name__ == '__main__':
    app.run(debug=True)