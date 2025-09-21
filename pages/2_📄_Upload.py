import streamlit as st
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.parser import parse_resume

DB_NAME = 'hackathon.db'

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
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO jobs (title, company, description_text) VALUES (?, ?, ?)",
                    (jd_title, jd_company, jd_text)
                )
                conn.commit()
                conn.close()
                st.success("Job Description added successfully!")
            except Exception as e:
                st.error(f"Database error: {e}")

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
                temp_path = os.path.join("uploads", resume_file.name)
                with open(temp_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                
                resume_text = parse_resume(temp_path)
                os.remove(temp_path)

                if resume_text:
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO resumes (candidate_name, email, text_content) VALUES (?, ?, ?)",
                            (candidate_name, candidate_email, resume_text)
                        )
                        conn.commit()
                        conn.close()
                        st.success("Resume added successfully!")
                    except Exception as e:
                        st.error(f"Database error: {e}")
                else:
                    st.error("Failed to extract text from the resume file.")