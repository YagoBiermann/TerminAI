import json
import os
from dotenv import load_dotenv
from src.rules import rules

load_dotenv()

def load_file(path):
  try:
    with open(path, "r") as f:
      file = json.load(f)
      return file
    
  except FileNotFoundError:
      return None

file_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(file_path)
persona_path = os.path.join(root_path, "personas.json")
personas = load_file(persona_path)

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

persona_description += rules