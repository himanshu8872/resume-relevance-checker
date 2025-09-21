# app/analyzer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def get_gemini_response(resume_text, jd_text):
    """
    Uses the Gemini Pro model to analyze the resume against the job description.
    """
    # Load environment variables from the .env file
    load_dotenv()

    # Configure the generative AI model
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in the .env file.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        return f"Error configuring the AI model: {e}"

    # This is our prompt. It's the detailed instruction we give to the AI.
    # We are asking it to act as a skilled tech recruiter.
    prompt = f"""
    Act as an expert and highly experienced ATS (Applicant Tracking System) with deep knowledge of the tech industry, 
    software engineering, and data science. Your task is to evaluate a candidate's resume against a given job description.

    **Job Description:**
    ---
    {jd_text}
    ---

    **Candidate's Resume:**
    ---
    {resume_text}
    ---

    **Evaluation Task:**
    Provide a detailed analysis of the resume's suitability for the job. Your output must be a single block of text with the following sections, clearly labeled with bold headings:

    **Relevance Score:** A percentage score from 0% to 100% indicating how well the resume matches the job description.

    **Verdict:** A single-word verdict: "High Suitability", "Medium Suitability", or "Low Suitability".

    **Missing Elements:** A bulleted list of key skills, technologies, or experiences mentioned in the job description that are missing from the resume. If nothing is missing, state "All key requirements are met."

    **Summary:** A brief, 2-3 sentence summary explaining the rationale behind your verdict and score. Highlight the candidate's key strengths and weaknesses for this specific role.

    **Feedback for Student:** A short, constructive, and personalized paragraph of feedback for the student, suggesting specific areas for improvement to better align with this type of job role in the future.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response from AI model: {e}"