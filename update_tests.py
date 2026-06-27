with open("tests/test_schemas.py", "r") as f:
    content = f.read()

import re

# Update valid request test
content = re.sub(r"        request = MealPlanRequest\(\n            dietary_preferences=\"vegetarian\",\n            budget=500\.0,\n            num_people=2,\n            day_context=\"Busy workday, need quick meals\",\n        \)\n        assert request\.dietary_preferences == \"vegetarian\"\n        assert request\.budget == 500\.0\n        assert request\.num_people == 2", """        request = MealPlanRequest(
            day_type="Busy workday",
            diet="Vegetarian",
            cuisine="Indian",
            budget=500.0,
            num_people=2,
            ingredients_at_home="rice, dal",
        )
        assert request.diet == "Vegetarian"
        assert request.budget == 500.0
        assert request.num_people == 2""", content)

# Update budget tests
content = re.sub(r"                dietary_preferences=\"any\",\n                budget=0,\n                num_people=2,\n                day_context=\"test\",", """                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=0,
                num_people=2,""", content)

content = re.sub(r"                dietary_preferences=\"any\",\n                budget=-100,\n                num_people=2,\n                day_context=\"test\",", """                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=-100,
                num_people=2,""", content)

content = re.sub(r"                dietary_preferences=\"any\",\n                budget=500,\n                num_people=0,\n                day_context=\"test\",", """                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=0,""", content)

content = re.sub(r"                dietary_preferences=\"any\",\n                budget=500,\n                num_people=21,\n                day_context=\"test\",", """                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=21,""", content)

content = re.sub(r"    def test_day_context_max_length\(self\) -> None:\n        \"\"\"Day context exceeding 1000 characters should be rejected\.\"\"\"\n        with pytest\.raises\(ValidationError\):\n            MealPlanRequest\(\n                dietary_preferences=\"any\",\n                budget=500,\n                num_people=2,\n                day_context=\"x\" \* 1001,\n            \)", """    def test_ingredients_max_length(self) -> None:
        \"\"\"Ingredients exceeding 1000 characters should be rejected.\"\"\"
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=2,
                ingredients_at_home="x" * 1001,
            )""", content)

content = re.sub(r"    def test_dietary_preferences_max_length\(self\) -> None:\n        \"\"\"Dietary preferences exceeding 500 characters should be rejected\.\"\"\"\n        with pytest\.raises\(ValidationError\):\n            MealPlanRequest\(\n                dietary_preferences=\"x\" \* 501,\n                budget=500,\n                num_people=2,\n                day_context=\"test\",\n            \)", "", content)

with open("tests/test_schemas.py", "w") as f:
    f.write(content)
