import re
skill_set = {
    "python", "sql", "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow",
    "opencv", "yolo", "nlp", "json", "api", "rest api", "git", "github",
    "flask", "fastapi", "debugging", "problem solving", "oop",
    "computer vision", "cvat", "data processing", "prompt engineering"}

def clean_txt(txt):
    txt = txt.lower()
    txt = re.sub(r'[^a-zA-Z0-9\s]', ' ', txt)
    return txt

def extract_skill(txt):
    cleaned_txt = clean_txt(txt)
    found_skill = set()
    for skill in skill_set:
        if skill in cleaned_txt:
            found_skill.add(skill)
    return list(found_skill)        
