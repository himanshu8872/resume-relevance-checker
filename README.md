# 🤖 AI-Powered Resume Relevance Check System

A full-stack web application built for the Innomatics Research Labs Hackathon to automate the resume evaluation process.

**[https://resume-relevance-checker-ngkya7s8ixqhae59hpdjrp.streamlit.app/]**

---

## 📝 Problem Statement

At Innomatics Research Labs, resume evaluation is currently manual, inconsistent, and time-consuming. Every week, the placement team across Hyderabad, Bangalore, Pune, and Delhi NCR receives 18–20 job requirements, with each posting attracting thousands of applications. This manual process leads to delays, inconsistent judgments, and a high workload for the placement team. The objective is to build a scalable and consistent automated system to solve this problem.

---

## 💡 Our Solution & Approach

We developed a full-stack application that leverages a Large Language Model (LLM) to provide nuanced, intelligent analysis of resumes against job descriptions. The system is designed with a professional client-server architecture to ensure scalability and maintainability.

* **Backend API (Flask):** A robust backend built with Flask serves as the application's "brain." It handles all business logic, including parsing uploaded documents, communicating with the database, and processing requests to the Google Gemini API for analysis.

* **Frontend Dashboard (Streamlit):** An interactive, multi-page dashboard built with Streamlit serves as the user interface for the placement team. It allows users to upload jobs and resumes, run evaluations, view a ranked candidate leaderboard for specific roles, and manage the underlying data.

* **Database (SQLite):** A lightweight SQLite database stores all jobs, resumes, and evaluation results, making the application stateful and allowing for features like analytics and leaderboards.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** Streamlit
* **AI Model:** Google Gemini
* **Database:** SQLite
* **Core Libraries:** Pandas, PyMuPDF, requests

---

## ⚙️ Installation & Usage

To run this project locally, please follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone [Your GitHub Repository URL Will Go Here]
    cd resume_analyzer
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your API Key**
    - Create a file named `.env` in the project's root directory.
    - Add your Google Gemini API key to this file:
      ```
      GOOGLE_API_KEY="Your-Key-Here"
      ```

5.  **Run the Application**
    - The application requires two terminals running simultaneously.
    - **In Terminal 1, start the Flask backend:**
      ```bash
      set FLASK_APP=main.py
      flask run
      ```
    - **In Terminal 2, start the Streamlit frontend:**
      ```bash
      streamlit run 1_🏠_Dashboard.py
      ```
    - The application will open automatically in your web browser.

---

## 🎥 Video Presentation

**[Your YouTube Video URL Will Go Here]**

---

## 👥 Team Members
* [Team Lead :- Himanshu Nandkishor Mahajan]
* [Team Member :- Aakash Pradeep Patil]
* [Team Member :- Bhushan Sanjay Desale]
