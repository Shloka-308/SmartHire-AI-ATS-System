from modules.resume_parser import parse_resume
from modules.jd_parser import parse_job_description
from modules.skill_extractor import extract_skill
from modules.ranker import rank_resume

resume_txt = parse_resume("resumes\Shloka_Acharya_Resume.pdf")
jd_txt = parse_job_description("jd\Job Title.pdf")

print("========== RESUME TEXT ==========")
print(resume_txt[:1000])

print("\n========== JD TEXT ==========")
print(jd_txt[:1000])

resume_skills = exract_skill(resume_txt)
jd_skills = extract_skill(jd_txt)

print("\n========== RESUME SKILLS ==========")
print(resume_skills)

print("\n========== JD SKILLS ==========")
print(jd_skills)

renk_result = rank_resume(resume_txt ,jd_txt , resume_skills ,jd_skills)

print("\n========== RANKING RESULT ==========")
print(renk_result)