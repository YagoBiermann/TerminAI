import os
import sys
from typing import Optional
from openai import OpenAI
import openai
from pydantic import BaseModel
from constants import API_CONNECTION_ERROR_MESSAGE, DEFAULT_ERROR_MESSAGE, LIMIT_REACHED_ERROR_MESSAGE
from display_messages import display_ai_response

global OpenAIClient
class AIResponse(BaseModel):
  is_powershell_command: bool
  powershell_command: Optional[str] = None
  response: str
  
def connect_to_openAI():
  try:
    return OpenAI(api_key=os.getenv("API_KEY"))
  except OpenAI.APIConnectionError:
    print("Unable to connect to OpenAI")

def call_ai(messages: list):
  try:
    response = OpenAIClient.beta.chat.completions.parse(
        model=os.getenv("MODEL"),
        store=False,
        messages = messages,
        temperature=float(os.getenv("TEMPERATURE")),
        max_tokens=250,
        response_format=AIResponse
    )
    ai_response = response.choices[0].message.parsed
    return ai_response
  
  except openai.APIConnectionError:
    display_ai_response(API_CONNECTION_ERROR_MESSAGE)
    sys.exit(1)
  except openai.RateLimitError:
    display_ai_response(LIMIT_REACHED_ERROR_MESSAGE)
    sys.exit(1)
  except Exception:
    display_ai_response(DEFAULT_ERROR_MESSAGE)
    sys.exit(1)
