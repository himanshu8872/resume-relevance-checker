# This script will run a full analysis of a resume against a JD

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.parser import parse_resume
from app.analyzer import get_gemini_response

def run_full_analysis():
    # Define paths for the resume and job description
    resume_path = os.path.join('uploads', 'resume - 1.pdf')
    jd_path = os.path.join('uploads', 'sample_jd_1.pdf')

    print("--- 1. Parsing Files ---")

    # Parse the resume
    resume_text = parse_resume(resume_path)
    if not resume_text:
        print(f"❌ FAILED to parse resume: {resume_path}")
        return
    print("✅ Resume parsed successfully.")

    # We can reuse our parser for the JD as well
    jd_text = parse_resume(jd_path)
    if not jd_text:
        print(f"❌ FAILED to parse job description: {jd_path}")
        return
    print("✅ Job Description parsed successfully.")

    print("\n--- 2. Sending to AI for Analysis (this may take a moment) ---")

    # Get the analysis from the Gemini API
    analysis_result = get_gemini_response(resume_text, jd_text)

    print("\n--- 3. 🤖 AI Analysis Complete! ---")
    print("-----------------------------------------")
    print(analysis_result)
    print("-----------------------------------------")

if __name__ == "__main__":
    run_full_analysis()