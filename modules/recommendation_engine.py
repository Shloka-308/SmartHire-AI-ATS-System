def generate_recommendation(missing_skills):
    recommendations = []
    for skill in missing_skills:

        if skill == "fastapi":
            recommendations.append("Learn FastAPI for backend API development.")

        elif skill == "flask":
            recommendations.append("Build Flask projects to improve backend development skills.")

        elif skill == "rest api":
            recommendations.append("Understand REST API concepts and API integration.")

        elif skill == "sql":
            recommendations.append("Practice advanced SQL queries and joins.")

        else:
            recommendations.append(f"Improve knowledge of {skill}.")

    return recommendations