with open("static/style.css", "r") as f:
    content = f.read()

content = content.replace(""".form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-lg);
}""", """.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-lg);
}

.form-row--3 {
  grid-template-columns: 1fr 1fr 1fr;
}""")

with open("static/style.css", "w") as f:
    f.write(content)
