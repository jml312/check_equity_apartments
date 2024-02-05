from requests import get
from bs4 import BeautifulSoup
from helpers.get_apartment_details import get_apartment_details
from helpers.get_special_details import get_special_details
from helpers.format_listing import format_listings
from helpers.get_building import get_building
from helpers.send_email import send_email

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
        building = get_building(apartment.text.split(" "), apartment_link["multi_options"])
        apartment_data.append({
          **apartment_details,
          **special_offer,
          **building
        })
        
    # sort by availability date, then price
    apartment_data = sorted(apartment_data, key=lambda el: (el["available"], int(el["price"].replace(",", "").replace("$", ""))))        
    
    listings.append({
      "apartment": apartment_link,
      "listings": apartment_data
    })

  formatted_listings = format_listings(listings)
  
  return send_email("Today's Apartment Listings 🏠", formatted_listings)