with open("routes/meal_planner.py", "r") as f:
    content = f.read()

content = content.replace("""    if len(request.dietary_preferences.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dietary preferences cannot be empty.",
        )
    if len(request.day_context.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Day context cannot be empty.",
        )""", """    if len(request.day_type.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Day type cannot be empty.",
        )
    if len(request.diet.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Diet cannot be empty.",
        )
    if len(request.cuisine.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cuisine cannot be empty.",
        )""")

content = content.replace("""        request.dietary_preferences[:50],""", """        request.diet[:50],""")

with open("routes/meal_planner.py", "w") as f:
    f.write(content)
