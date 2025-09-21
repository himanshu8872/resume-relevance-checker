import streamlit as st
import requests
import os
import sys

# This allows us to import our parser function from the 'app' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.parser import parse_resume

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Upload Data", layout="wide")
st.title("📄 Upload New Data")
st.info("Use this page to add new Job Descriptions and Resumes to the system's database.")

# --- Job Description Uploader ---
st.subheader("1. Add a Job Description")
with st.form("jd_form", clear_on_submit=True):
    jd_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
    jd_company = st.text_input("Company Name", placeholder="e.g., Tech Corp Inc.")
    
    jd_text = st.text_area("Paste Job Description Text Here", height=200)
    
    submitted_jd = st.form_submit_button("Add Job to Database")

    if submitted_jd:
        if not jd_title or not jd_text.strip():
            st.warning("Job Title and Description Text are required.")
        else:
            with st.spinner("Processing..."):
                payload = {
                    "title": jd_title,
                    "company": jd_company,
                    "description_text": jd_text
                }
                try:
                    response = requests.post(f"{API_URL}/jobs", json=payload)
                    if response.status_code == 201:
                        st.success("Job Description added successfully!")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not connect to the backend server.")

st.divider()

# --- Resume Uploader ---
st.subheader("2. Add a Candidate Resume")
with st.form("resume_form", clear_on_submit=True):
    candidate_name = st.text_input("Candidate Name", placeholder="e.g., John Smith")
    candidate_email = st.text_input("Candidate Email (Optional)", placeholder="e.g., john.smith@email.com")
    resume_file = st.file_uploader("Upload Resume File", type=["pdf", "docx"], label_visibility="collapsed")

    submitted_resume = st.form_submit_button("Add Resume to Database")
    
    if submitted_resume:
        if not candidate_name or not resume_file:
            st.warning("Candidate Name and a resume file are required.")
        else:
            with st.spinner("Processing..."):
                # We need a temporary place to save the file to parse it
                temp_path = os.path.join("uploads", resume_file.name)
                with open(temp_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                
                resume_text = parse_resume(temp_path)
                os.remove(temp_path) # Clean up the temporary file

                if resume_text:
                    payload = {
                        "candidate_name": candidate_name,
                        "email": candidate_email,
                        "text_content": resume_text
                    }
                    try:
                        response = requests.post(f"{API_URL}/resumes", json=payload)
                        if response.status_code == 201:
                            st.success("Resume added successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Connection Error: Could not connect to the backend server.")
                else:
                    st.error("Failed to extract text from the resume file.")