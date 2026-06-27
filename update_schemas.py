with open("models/schemas.py", "r") as f:
    content = f.read()

content = content.replace("""    dietary_preferences: str = Field(
        ...,
        max_length=500,
        description="Dietary preferences or restrictions (e.g., 'vegetarian, gluten-free').",
    )""", """    day_type: str = Field(
        ...,
        description="Type of day (e.g., 'Busy workday', 'Relaxed weekend').",
    )
    diet: str = Field(
        ...,
        description="Dietary preferences (e.g., 'Vegetarian', 'Vegan').",
    )
    cuisine: str = Field(
        ...,
        description="Cuisine preference (e.g., 'Indian', 'Continental').",
    )""")

content = content.replace("""    day_context: str = Field(
        ...,
        max_length=1000,
        description="Context about the day to help tailor meals (e.g., 'busy workday, need quick meals').",
    )""", """    ingredients_at_home: str = Field(
        default="",
        max_length=1000,
        description="Ingredients available at home (e.g., 'rice, onions, tomatoes').",
    )""")

with open("models/schemas.py", "w") as f:
    f.write(content)
