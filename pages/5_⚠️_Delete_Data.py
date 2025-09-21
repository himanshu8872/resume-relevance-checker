import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = 'hackathon.db'
st.set_page_config(page_title="Delete Data", layout="centered")
st.title("⚠️ Delete Data")
st.warning("Warning: Deleting a job or resume will also delete all of its associated evaluations permanently.")

def delete_job(job_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
    st.success("Job deleted successfully!")

def delete_resume(resume_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        conn.commit()
    st.success("Resume deleted successfully!")

try:
    with sqlite3.connect(DB_NAME) as conn:
        jobs_data = conn.execute("SELECT id, title, company FROM jobs").fetchall()
        resumes_data = conn.execute("SELECT id, candidate_name FROM resumes").fetchall()

    st.divider()
    
    # --- Delete Job Section ---
    st.subheader("Delete a Job Description")
    if not jobs_data:
        st.info("No jobs to delete.")
    else:
        for job_id, title, company in jobs_data:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.text(f"{title} at {company}")
            with col2:
                # Each button has a unique key to identify the specific job
                if st.button("Delete", key=f"job_{job_id}"):
                    delete_job(job_id)
                    st.rerun()

    st.divider()

    # --- Delete Resume Section ---
    st.subheader("Delete a Resume")
    if not resumes_data:
        st.info("No resumes to delete.")
    else:
        for resume_id, name in resumes_data:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.text(name)
            with col2:
                # Each button has a unique key to identify the specific resume
                if st.button("Delete", key=f"resume_{resume_id}"):
                    delete_resume(resume_id)
                    st.rerun()

except Exception as e:
    st.error(f"An error occurred: {e}")