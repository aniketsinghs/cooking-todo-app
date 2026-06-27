with open("services/gemini_service.py", "r") as f:
    content = f.read()

content = content.replace("""    return f\"\"\"You are a professional meal planner and nutritionist. Generate a complete daily meal plan based on the following requirements:

**Dietary Preferences:** {request.dietary_preferences}
**Budget:** ₹{request.budget:.2f}
**Number of People:** {request.num_people}
**Day Context:** {request.day_context}""", """    return f\"\"\"You are a professional meal planner and nutritionist. Generate a complete daily meal plan based on the following requirements:

**Day Type:** {request.day_type}
**Diet:** {request.diet}
**Cuisine:** {request.cuisine}
**Ingredients at Home:** {request.ingredients_at_home}
**Budget:** ₹{request.budget:.2f}
**Number of People:** {request.num_people}""")

with open("services/gemini_service.py", "w") as f:
    f.write(content)
