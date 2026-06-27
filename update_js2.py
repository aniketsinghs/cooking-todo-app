with open("static/app.js", "r") as f:
    content = f.read()

import re

# Update Form Submission Payload - correctly matching the actual content
form_submit_search = r"    // Validate\n    const context = dayContext\.value\.trim\(\);\n    const budget  = parseFloat\(budgetInput\.value\);\n    const people  = parseInt\(numPeopleInput\.value, 10\);\n\n    if \(\!context\) \{\n      showError\('Please describe your day so we can plan meals for you\.'\);\n      dayContext\.focus\(\);\n      return;\n    \}\n\n    if \(isNaN\(budget\) \|\| budget <= 0\) \{\n      showError\('Please enter a valid budget greater than ₹0\.'\);\n      budgetInput\.focus\(\);\n      return;\n    \}\n\n    if \(isNaN\(people\) \|\| people < 1 \|\| people > 20\) \{\n      showError\('Number of people must be between 1 and 20\.'\);\n      numPeopleInput\.focus\(\);\n      return;\n    \}\n\n    // Build payload\n    const payload = \{\n      day_context: context,\n      dietary_preferences: dietaryPrefs\.value\.trim\(\),\n      budget: budget,\n      num_people: people,\n    \};"
form_submit_replace = """    // Validate
    const typeOfDay = dayType.value;
    const dietVal   = diet.value;
    const cuisineVal = cuisine.value;
    const homeIng   = ingredientsHome.value.trim();
    const budget    = parseFloat(budgetInput.value);
    const people    = parseInt(numPeopleInput.value, 10);

    if (isNaN(budget) || budget <= 0) {
      showError('Please enter a valid budget greater than ₹0.');
      budgetInput.focus();
      return;
    }

    if (isNaN(people) || people < 1 || people > 20) {
      showError('Number of people must be between 1 and 20.');
      numPeopleInput.focus();
      return;
    }

    // Build payload
    const payload = {
      day_type: typeOfDay,
      diet: dietVal,
      cuisine: cuisineVal,
      ingredients_at_home: homeIng,
      budget: budget,
      num_people: people,
    };"""

content = re.sub(form_submit_search, form_submit_replace, content)

# Remove the focus call to the non-existing dayContext variable that might have been missed
content = content.replace("dayContext.focus();", "")

with open("static/app.js", "w") as f:
    f.write(content)
