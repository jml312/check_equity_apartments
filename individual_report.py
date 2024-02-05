from requests import get
from bs4 import BeautifulSoup
from helpers.get_apartment_details import get_apartment_details
from helpers.get_special_details import get_special_details
from helpers.format_listing import format_listings
from helpers.send_email import send_email

def individual_report(apartment_link, apartment_details):  
  try:
    price, beds, baths, availability, sqft, floors = apartment_details["price"], apartment_details["beds"], apartment_details["baths"], apartment_details["availability"],apartment_details["sqft"],apartment_details["floors"]   
    
    res = get(apartment_link["url"])
      
    soup = BeautifulSoup(res.content, 'html.parser')
    
    all_apartments = soup.find_all("div", class_="unit-expanded-card")
    
    apartment_data = []
    for apartment in all_apartments:
      specs = apartment.find("div", class_="specs")
      text_data = [data for data in specs.text.split(" ") if data]
      
      _, details = get_apartment_details(text_data, {}, False)
      special = get_special_details(apartment)
      
      found_price, found_beds, found_baths, found_availability, found_sqft, found_floor = details["price"][1:], details["beds"], details["baths"], details["available"], details["sq_ft"],details["floor_num"] 
      
      if price == found_price.replace(",", "") and beds == found_beds and baths == found_baths and availability == found_availability.strftime("%m/%d/%Y") and sqft == found_sqft and found_floor in floors:
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
    
    
    