import os
from nylas import APIClient

def send_email(title, formatted_listings):
  CLIENT_ID = os.getenv("NYLAS_CLIENT_ID")
  CLIENT_SECRET = os.getenv("NYLAS_CLIENT_SECRET")
  ACCESS_TOKEN = os.getenv("NYLAS_ACCESS_TOKEN")
  
  nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN
  )
  
  try:
    draft = nylas.drafts.create()
    draft.subject = title    
    draft.body = formatted_listings
    draft.to = [
      {'name': 'Catherine (personal)', 'email': 'catherinefelix@hotmail.com'},
      {'name': 'Catherine (work)', 'email': 'cmailly@navatx.com'},
      {'name': 'Josh', 'email': 'joshlevy.texas@gmail.com'},
    ]
    draft.send()
    return "Report sent ✅", 200
  except Exception as e:
    return f"Error: {e}", 400