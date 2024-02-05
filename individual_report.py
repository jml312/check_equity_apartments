from requests import get
from bs4 import BeautifulSoup
from helpers.get_apartment_details import get_apartment_details
from helpers.get_special_details import get_special_details
from helpers.format_listing import format_listings
from helpers.send_email import send_email

def individual_report(apartment_link, apartment_details):  
  try:
    beds, baths, sqft = apartment_details["beds"], apartment_details["baths"], apartment_details["sqft"]   
    
    res = get(apartment_link["url"])
      
    soup = BeautifulSoup(res.content, 'html.parser')
    
    all_apartments = soup.find_all("div", class_="unit-expanded-card")
    
    apartment_data = []
    for apartment in all_apartments:
      specs = apartment.find("div", class_="specs")
      text_data = [data for data in specs.text.split(" ") if data]
      
      _, details = get_apartment_details(text_data, {}, False)
      special = get_special_details(apartment)
      
      found_beds, found_baths, found_sqft = details["beds"], details["baths"], details["sq_ft"] 
      
      if beds == found_beds and baths == found_baths and sqft == found_sqft:
       apartment_data.append({
         **details,
         "special_offer": special,
         "building": apartment_details["building"]
       }) 
       
    listings = [
      {
        "apartment": {
          "name": apartment_link["name"],
          "url": apartment_link["url"],
          },
        "listings": apartment_data,
      }
    ]
    
    formatted_listings = format_listings(listings)
    
    return send_email(f"{apartment_link['name']} Update 🚀", formatted_listings)
  except Exception as e:
    return f"Error: {e}", 400
    
    
    