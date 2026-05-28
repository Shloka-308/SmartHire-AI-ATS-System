import streamlit as st
import os
from modules.resume_parser import parse_resume
from modules.jd_parser import parse_job_description 
from modules.skill_extractor import extract_skill
from modules.ranker import rank_resume
from modules.recommendation_engine import generate_recommendation
import pandas as pd
import json

os.makedirs("resumes", exist_ok=True)
os.makedirs("jd", exist_ok=True)
os.makedirs("applications",exist_ok=True)

#page visualization
st.set_page_config(
    page_title="SMART HIRE",
    layout="wide",
    page_icon="🚀"
)
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Title */
h1, h2, h3 {
    color: #00FFAA;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 10px;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #00CC88;
    color: white;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #00FFAA;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: bold;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("🚀 SMART HIRE")
st.sidebar.write("AI Recruitment Platform")
#tab
candidate_tab ,hr_tab = st.tabs(["👨‍💻 Candidate Portal", "👨‍💼 HR Dashboard"])

#candidate dashboard
with candidate_tab:
    st.title("🚀 SMART HIRE")
    st.markdown("""
### AI-Powered Resume Screening Platform

Analyze resumes, match job roles, and improve ATS compatibility using AI & NLP.
""")
    st.caption("AI-Powered ATS Resume Screening Platform")
    st.write("Upload your resume and your target role to check ATS compatibility and improve your chances.")
    st.subheader("📄 Upload Resume")
    st.divider()
    with open("jobs.json","r") as f:
        jobs = json.load(f)
    resume_file = st.file_uploader("Upload Resume",type=["pdf","docx"])
    if jobs:
        selected_role = st.selectbox("Select Role",list(jobs.keys()))
    else:
        st.warning("No job openings available.")
    if st.button("Analyze Candidate"):
        if resume_file:
            jd_path = jobs[selected_role]
            resume_path = os.path.join("resumes", resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.getbuffer())

            resume_txt = parse_resume(resume_path)
            jd_txt = parse_job_description(jd_path)
            resume_skills = extract_skill(resume_txt)
            jd_skills = extract_skill(jd_txt)
            result = rank_resume(resume_txt,jd_txt,resume_skills,jd_skills)  
            recommendation = generate_recommendation(result["missing_skills"]) 

            st.subheader("Analysis Report")
            st.divider()
            score = result["final_ranking_score"]

            if score >= 75:
                st.success("Excellent ATS Match ✅")

            elif score >= 50:
                st.warning("Moderate ATS Match ⚠️")

            else:
                st.error("Low ATS Match ❌")

            col1,col2,col3 = st.columns(3)
            with col1:
                st.metric("🎯 Final ATS Score",f"{result['final_ranking_score']}%" )
            with col2:
                st.metric("🛠 Skill match",f"{result['skill_match_score']}%")    
            with col3:
                st.metric("🧠 Semantic Score",f"{result['semantic_similarity_score']}%")
            st.write("ATS Compatibility")
            st.progress( int(result['final_ranking_score']))    

            col1,col2 = st.columns(2)
            with col1:
                st.write("✅ Common Skills")
                st.success(result["common_skills"])
            with col2:
                st.write("❌ Missing Skills")
                st.error(result["missing_skills"])    
            
            st.subheader("Recommendation")
            for rec in recommendation:
                st.success(f"💡{rec}")

        else:
            st.warning("Please upload a Resume.")    

#hr dashboard        
with hr_tab:
    st.title("👨‍💼 HR Dashboard")
    st.caption("Manage job openings and rank candidates intelligently")
    st.write( "Upload a Job Description and multiple resumes to rank candidates.")
    st.subheader("📢 Publish Job Opening")
    st.divider()
    job_role = st.text_input("Enter Job Role")
    hr_jd_file = st.file_uploader("Upload Job Description",type=["pdf","docx"],key="publish_jd")

    if st.button("Publish Job Opening"):
        if job_role and hr_jd_file:
            jd_path = jobs[selected_role]
            with open("jobs.json","r") as f:
                jobs = json.load(f)
            jobs[job_role] = jd_path   
            with open("jobs.json", "w") as f:
                json.dump(jobs, f)        
            st.success(f"{job_role} job opening published successfully!")    
    with open("jobs.json", "r") as f:
        jobs = json.load(f)
    selected_hr_role = st.selectbox("Select Published Role",list(jobs.keys()),key="hr_role_select")
    application_folder = os.path.join("applications",selected_hr_role)
    resume_files = os.listdir(application_folder)
    if not os.path.exists(application_folder):
        st.warning("No applications received yet.")
        st.stop()

    top_n = st.number_input("Number of candidates to shortlist",min_value=1,value=3,step=1)
    if st.button("Rank Candidate"):
        if selected_hr_role:
            jd_path = jobs[selected_hr_role]
            jd_txt = parse_job_description(jd_path)  
            jd_skills = extract_skill(jd_txt)  
            application_folder = os.path.join("applications",selected_hr_role)
            resume_files = os.listdir(application_folder)
            all_results = []
            seen_resumes = set()
            for file_name in resume_files:
                if file_name in seen_resumes:
                    st.warning(f"Duplicate resume detected : "f"{resume_file.name}")
                    continue   
                seen_resumes.add(file_name)           

                role_folder = os.path.join("applications",selected_role)
                os.makedirs(role_folder, exist_ok=True)

                resume_path = os.path.join(application_folder, file_name)
                with open(resume_path,"wb") as f:
                    f.write(resume_file.getbuffer())
                resume_txt = parse_resume(resume_path)
                resume_skills = extract_skill(resume_txt)
                result = rank_resume(resume_txt,jd_txt,resume_skills,jd_skills)    
                all_results.append({
                    "candidate_name" : file_name,
                    "score" : result["final_ranking_score"],
                    "common_skills" : result["common_skills"],
                    "missing_skills" : result["missing_skills"]
                })

            # ranking
            sorted_result = sorted(all_results,key=lambda x:x["score"],reverse=True)
            sortlisted_candidate = sorted_result[:top_n]
            df = pd.DataFrame(sorted_result)
            st.subheader("Shortlisted Candidates")
            st.divider()
            for idx, candidate in enumerate(sortlisted_candidate,start=1):
                st.success(
                    f"{idx}. "
                    f"{candidate['candidate_name']} "
                    f"- {candidate['score']}%"
                )

            #score cards
            st.subheader("🏆 Candidate Ranking")  
            st.divider()
            cols = st.columns(3)
            for idx,candidate in enumerate(sorted_result):
                with cols[idx % 4]:
                    st.markdown(
                    f""" <div style="border:1px solid #444;
                    border-radius:15px;
                    padding:20px;
                    margin-bottom:20px;
                    background-color:#1e1e1e;
                    box-shadow:0 4px 12px rgba(0,0,0,0.4);
                    transition:0.3s;">
                    <h4>🏆 Rank #{idx+1}</h4>
                    <h3>{candidate['candidate_name']}</h3>
                    <h2 style="color:#00ff99;">
                        {candidate['score']}%
                    </h2>
                    <p>
                    <b>Missing Skills:</b><br>
                    {", ".join(candidate['missing_skills'])}
                    </p>
                    </div>""",
                    unsafe_allow_html=True)

            st.bar_chart(df.set_index("candidate_name")["score"])        
            
            #analytics
            if sorted_result:        
                total_candidate = len(sorted_result)
                highest_score = sorted_result[0]["score"]
                avg_score = round(sum(candidate["score"] for candidate in sorted_result)/ total_candidate,2)     
                st.subheader("📊 HR Analytics Dashboard")
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Candidates", total_candidate)
                with col2:
                    st.metric("Highest ATS Score", f"{highest_score}%")
                with col3:
                    st.metric("Average ATS Score", f"{avg_score}%")   

            #result table    
            st.subheader("Candidate Ranking Table")   
            st.divider() 
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download HR Report CSV",data = csv, file_name="candidate_rankings.csv",mime="text/csv")

        else:
            st.warning("Please upload Resumes.")    