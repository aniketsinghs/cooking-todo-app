with open("static/index.html", "r") as f:
    content = f.read()

import re

# We will replace the entire form inner html up to the submit button
search_pattern = re.compile(r'<!-- Day Context -->.*?<!-- Submit -->', re.DOTALL)
replacement = """<!-- Top Row: Day Type, Diet, Cuisine -->
          <div class="form-row form-row--3">
            <div class="form-group">
              <label for="day-type" class="form-label">
                Day type
              </label>
              <select id="day-type" name="day_type" class="form-control" aria-label="Select day type" required>
                <option value="Busy workday">Busy workday</option>
                <option value="Relaxed weekend">Relaxed weekend</option>
                <option value="Work from home">Work from home</option>
                <option value="Special occasion">Special occasion</option>
              </select>
            </div>

            <div class="form-group">
              <label for="diet" class="form-label">
                Diet
              </label>
              <select id="diet" name="diet" class="form-control" aria-label="Select diet" required>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Non-vegetarian">Non-vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Eggetarian">Eggetarian</option>
              </select>
            </div>

            <div class="form-group">
              <label for="cuisine" class="form-label">
                Cuisine
              </label>
              <select id="cuisine" name="cuisine" class="form-control" aria-label="Select cuisine" required>
                <option value="Indian">Indian</option>
                <option value="Bengali">Bengali</option>
                <option value="Continental">Continental</option>
                <option value="Mixed">Mixed</option>
              </select>
            </div>
          </div>

          <!-- Bottom Row: People, Budget, Ingredients at home -->
          <div class="form-row form-row--3">
            <div class="form-group">
              <label for="num-people" class="form-label">
                People
              </label>
              <input
                type="number"
                id="num-people"
                name="num_people"
                class="form-control"
                value="2"
                min="1"
                max="20"
                aria-label="Number of people to cook for"
                aria-required="true"
                required
              />
            </div>

            <div class="form-group">
              <label for="budget" class="form-label">
                Daily budget (₹)
              </label>
              <input
                type="number"
                id="budget"
                name="budget"
                class="form-control"
                value="500"
                min="1"
                step="10"
                aria-label="Budget in Indian Rupees"
                aria-required="true"
                required
              />
            </div>

            <div class="form-group">
              <label for="ingredients-home" class="form-label">
                Ingredients at home
              </label>
              <input
                type="text"
                id="ingredients-home"
                name="ingredients_at_home"
                class="form-control"
                maxlength="500"
                placeholder="rice, onions, tomatoes"
                aria-label="Enter ingredients available at home"
              />
            </div>
          </div>

          <!-- Submit -->"""
content = search_pattern.sub(replacement, content)

# Update submit button
content = content.replace("""<span class="btn__text">✨ Generate Meal Plan</span>""", """<span class="btn__text">✨ Generate cooking plan ↗</span>""")

with open("static/index.html", "w") as f:
    f.write(content)
