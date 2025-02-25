import json
import os
from dotenv import load_dotenv
load_dotenv()

def load_file(path):
  try:
    with open(path, "r") as f:
      file = json.load(f)
      return file
    
  except FileNotFoundError:
      return None

file_path = os.path.dirname(os.path.abspath(__file__))
persona_path = os.path.join(file_path, "personas.json")
rules_path = os.path.join(file_path, "rules.json")

personas = load_file(persona_path)
rules = load_file(rules_path)

current_persona_key = os.getenv('CURRENT_PERSONA')
persona_description = ""

if personas and current_persona_key in personas:
    selected_persona = personas[current_persona_key]
    persona_description = f"""
    Your name is: {selected_persona['name']}
    Description: {selected_persona['description']}
    """
else:
  print(f"Warning: Persona '{current_persona_key}' not applied. Using default settings")

if rules:
  persona_description += "\n Response Rules:" + "".join(f"\n- {rules}" for rules in rules['rules'])
else:
  print(f"Warning: rules.json not found. Rules not applied.")
  rules = ""