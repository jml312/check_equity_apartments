from requests import get
from bs4 import BeautifulSoup
from helpers.get_apartment_details import get_apartment_details
from helpers.get_special_details import get_special_details
from helpers.format_listing import format_listings
import os
from nylas import APIClient

def apartment_report(apartment_links, apartment_criteria):  
  listings = []
  for apartment_link in apartment_links:
    res = get(apartment_link["url"])
    
    soup = BeautifulSoup(res.content, 'html.parser')
  
    all_apartments = soup.find_all("div", class_="unit-expanded-card") 
    
    apartment_data = []
    for apartment in all_apartments:
      specs = apartment.find("div", class_="specs")
      text_data = [data for data in specs.text.split(" ") if data]
      
      meets_criteria, apartment_details = get_apartment_details(text_data, apartment_criteria)
      if meets_criteria:
        special_offer = {
          "special_offer": get_special_details(apartment)
        }
        apartment_data.append({
          **apartment_details,
          **special_offer
        })
        
    # sort by availability date, then price
    apartment_data = sorted(apartment_data, key=lambda el: (el["available"], int(el["price"].replace(",", "").replace("$", ""))))        
    
    listings.append({
      "apartment": apartment_link,
      "listings": apartment_data
    })

  formatted_listings = format_listings(listings)
  
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
    draft.subject = "Today's Apartment Listings 🏠"    
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