with open("README.md", "r") as f:
    content = f.read()

content = content.replace("""{
  "dietary_preferences": "vegetarian, no nuts",
  "budget": 500.0,
  "num_people": 2,
  "day_context": "Busy workday, need quick and healthy meals"
}""", """{
  "day_type": "Busy workday",
  "diet": "Vegetarian",
  "cuisine": "Indian",
  "budget": 500.0,
  "num_people": 2,
  "ingredients_at_home": "rice, onions, tomatoes"
}""")

with open("README.md", "w") as f:
    f.write(content)
