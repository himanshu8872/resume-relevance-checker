import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = 'hackathon.db'
st.set_page_config(page_title="Delete Data", layout="centered")
st.title("⚠️ Delete Data")
st.warning("Warning: Deleting a job or resume will also delete all of its associated evaluations permanently.")

try:
    with sqlite3.connect(DB_NAME) as conn:
        jobs_data = conn.execute("SELECT id, title, company FROM jobs").fetchall()
        jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
        if not jobs_df.empty:
            jobs_df['display'] = jobs_df['title'] + " at " + jobs_df['company']

        resumes_data = conn.execute("SELECT id, candidate_name, email FROM resumes").fetchall()
        resumes_df = pd.DataFrame(resumes_data, columns=['id', 'name', 'email'])
        if not resumes_df.empty:
            resumes_df['display'] = resumes_df['name']

    st.divider()

    # --- Delete Job Section ---
    if not jobs_df.empty:
        st.subheader("Delete a Job Description")
        job_to_delete_display = st.selectbox("Select Job", options=jobs_df['display'], key="job_to_delete", index=None, placeholder="Choose a job to delete...")
        if st.button("Delete Job"):
            if job_to_delete_display:
                job_id = jobs_df[jobs_df['display'] == job_to_delete_display]['id'].iloc[0]
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute("PRAGMA foreign_keys = ON")
                    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
                    conn.commit()
                st.success(f"Deleted '{job_to_delete_display}' successfully!")
                st.rerun()
    else:
        st.info("No jobs to delete.")

    st.divider()

    # --- Delete Resume Section ---
    if not resumes_df.empty:
        st.subheader("Delete a Resume")
        resume_to_delete_display = st.selectbox("Select Resume", options=resumes_df['display'], key="resume_to_delete", index=None, placeholder="Choose a resume to delete...")
        if st.button("Delete Resume"):
            if resume_to_delete_display:
                resume_id = resumes_df[resumes_df['display'] == resume_to_delete_display]['id'].iloc[0]
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute("PRAGMA foreign_keys = ON")
                    conn.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
                    conn.commit()
                st.success(f"Deleted '{resume_to_delete_display}' successfully!")
                st.rerun()
    else:
        st.info("No resumes to delete.")

except Exception as e:
    st.error(f"An error occurred: {e}")