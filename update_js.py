with open("static/app.js", "r") as f:
    content = f.read()

import re

# Replace DOM references
dom_refs_search = r"  const dayContext        = document\.getElementById\('day-context'\);\n  const dayContextCount   = document\.getElementById\('day-context-count'\);\n  const dietaryPrefs      = document\.getElementById\('dietary-preferences'\);\n"
dom_refs_replace = """  const dayType           = document.getElementById('day-type');
  const diet              = document.getElementById('diet');
  const cuisine           = document.getElementById('cuisine');
  const ingredientsHome   = document.getElementById('ingredients-home');
"""
content = re.sub(dom_refs_search, dom_refs_replace, content)

# Remove character counter for dayContext
content = re.sub(r"  // ─── Character Counter ───\n  dayContext\.addEventListener\('input', \(\) => \{\n    dayContextCount\.textContent = dayContext\.value\.length;\n  \}\);\n\n", "", content)

# Update Form Submission Payload
form_submit_search = r"    const context = dayContext\.value\.trim\(\);\n    const prefs   = dietaryPrefs\.value\.trim\(\);\n    const budget  = parseFloat\((budgetInput|document\.getElementById\('budget'\))\.value\);\n    const people  = parseInt\((numPeopleInput|document\.getElementById\('num-people'\))\.value, 10\);\n\n    if \(\!context\) \{\n      showError\('Please tell us about your day so we can plan accordingly\.'\);\n      dayContext\.focus\(\);\n      return;\n    \}\n\n    const payload = \{\n      day_context: context,\n      dietary_preferences: prefs \|\| 'None',\n      budget: budget,\n      num_people: people,\n    \};"
form_submit_replace = """    const typeOfDay = dayType.value;
    const dietVal   = diet.value;
    const cuisineVal = cuisine.value;
    const homeIng   = ingredientsHome.value.trim();
    const budget    = parseFloat(budgetInput.value);
    const people    = parseInt(numPeopleInput.value, 10);

    const payload = {
      day_type: typeOfDay,
      diet: dietVal,
      cuisine: cuisineVal,
      ingredients_at_home: homeIng,
      budget: budget,
      num_people: people,
    };"""
content = re.sub(form_submit_search, form_submit_replace, content)

with open("static/app.js", "w") as f:
    f.write(content)
