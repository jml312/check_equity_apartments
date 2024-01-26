from apartment_report import apartment_report
from flask import Flask, request
from json import load
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def main():
  if request.args.get("secret") != os.getenv('SECRET'):
    return "Not authorized", 401

  with open("./data/apartment_links.json", "r") as jf:
    apartment_links = load(jf)
  with open("./data/apartment_criteria.json", "r") as jf:
    apartment_criteria = load(jf)  
    
    res, status_code = apartment_report(apartment_links, apartment_criteria)
    
    return res, status_code