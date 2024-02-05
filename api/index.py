from apartment_report import apartment_report
from individual_report import individual_report
from flask import Flask, request
from json import load
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def is_auth():
  return request.args.get("secret") == os.getenv('SECRET')
  

@app.route('/')
def home():
  if not is_auth():
    return "Not authorized", 401

  with open("./data/apartment_links.json", "r") as jf:
    apartment_links = load(jf)
  with open("./data/apartment_criteria.json", "r") as jf:
    apartment_criteria = load(jf)  
    
    res, status_code = apartment_report(apartment_links, apartment_criteria)
    
    return res, status_code

  
@app.route("/apartment")
def apartment():  
  if not is_auth():
    return "Not authorized", 401
  
  try:
    res, status_code = individual_report(apartment_link={
        "url": request.args.get("url"),
        "name": request.args.get("name"),
      }, apartment_details={
      "price": request.args.get("price"),
      "beds": request.args.get("beds"),
      "baths": request.args.get("baths"),
      "availability": request.args.get("availability"),
      "sqft": request.args.get("sqft"),
      "floors": request.args.get("floors").split(","),
      "building": request.args.get("building")
    })
    
    return res, status_code
  except Exception as e:
    return f"Error: {e}", 400
  
  