from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def skill_match_score(resume_skills,jd_skills):
    common_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))
    if len(jd_skills) == 0:
        score = 0
    else:
        score = (len(common_skills) / len(jd_skills)) * 100
    return common_skills ,missing_skills ,round(score,2)    

def semantic_similarity(resume_txt , jd_txt):
    documents = [resume_txt ,jd_txt]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])
    return round(similarity[0][0]* 100 ,2)

def rank_resume(resume_txt , jd_txt,resume_skills ,jd_skills):
    common_skills,missing_skills,skill_score = skill_match_score(resume_skills ,jd_skills)
    semantic_score = float(semantic_similarity(resume_txt,jd_txt))   #works on full text to compare semantic texual similarity
    final_score = float(round((0.6*skill_score) + (0.4*semantic_score),2))
    return { 
        "common_skills": common_skills,
        "missing_skills": missing_skills,
        "skill_match_score": skill_score,
        "semantic_similarity_score": semantic_score,
        "final_ranking_score": final_score}