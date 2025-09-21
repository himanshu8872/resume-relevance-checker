import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = 'hackathon.db'

st.set_page_config(page_title="Leaderboard", layout="wide")
st.title("🏆 Candidate Leaderboard")
st.info("Select a job to see all evaluated candidates ranked by their relevance score.")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    jobs_data = cursor.execute("SELECT id, title, company FROM jobs").fetchall()
    if not jobs_data:
        st.warning("No jobs found. Please add a job on the 'Upload' page first.")
    else:
        jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
        jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')
        
        selected_job_display = st.selectbox("Select a Job to see the candidate ranking:", jobs_df['display'])
        
        if selected_job_display:
            selected_job_id = jobs_df[jobs_df['display'] == selected_job_display]['id'].iloc[0]
            
            st.divider()
            st.subheader(f"Showing top candidates for: {selected_job_display}")

            query = """
                SELECT r.candidate_name, r.email, e.score, e.verdict
                FROM evaluations e JOIN resumes r ON e.resume_id = r.id
                WHERE e.job_id = ? ORDER BY e.score DESC
            """
            evaluations_data = cursor.execute(query, (int(selected_job_id),)).fetchall()

            if not evaluations_data:
                st.info("No evaluations have been run for this job yet.")
            else:
                leaderboard_df = pd.DataFrame(evaluations_data, columns=['candidate_name', 'email', 'score', 'verdict'])
                leaderboard_df['score'] = leaderboard_df['score'].map('{:.1f}%'.format)
                leaderboard_df.index = leaderboard_df.index + 1
                leaderboard_df.rename_axis('Rank', inplace=True)
                st.dataframe(leaderboard_df, use_container_width=True)

                # --- CORRECTED DELETE SECTION ---
                if not leaderboard_df.empty:
                    st.write("---")
                    st.subheader("Delete an Evaluation")
                    
                    eval_to_delete_name = st.selectbox("Select a candidate evaluation to remove:", options=leaderboard_df['candidate_name'], key="eval_select")
                    
                    if st.button("Delete Evaluation"):
                        if eval_to_delete_name:
                            # We need the full resumes list to find the ID from the name
                            resumes_data_for_delete = conn.execute("SELECT id, candidate_name FROM resumes").fetchall()
                            resumes_df_for_delete = pd.DataFrame(resumes_data_for_delete, columns=['id', 'name'])

                            resume_id_to_delete = resumes_df_for_delete[resumes_df_for_delete['name'] == eval_to_delete_name]['id'].iloc[0]
                            
                            try:
                                # Re-open connection for writing
                                conn_del = sqlite3.connect(DB_NAME)
                                conn_del.execute("DELETE FROM evaluations WHERE job_id = ? AND resume_id = ?", (int(selected_job_id), int(resume_id_to_delete)))
                                conn_del.commit()
                                conn_del.close()
                                st.success(f"Deleted evaluation for '{eval_to_delete_name}' successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete evaluation: {e}")

    conn.close()

except Exception as e:
    st.error(f"An error occurred: {e}")