def format_listings(listings):
  formatted_listing = ""
  for listing in listings:
    apartment, listing_data = listing["apartment"], listing["listings"]  
    url, name = apartment["url"], apartment["name"]
    formatted_listing += f"<b><a href={url}>{name}</a></b>"
    
    if not listing_data:
      formatted_listing += "<p>Sorry 😞</p>"
      continue
    
    formatted_listing += "<ul>"
    for ld in listing_data:
      price, term, beds, baths, sq_ft, floor_num, available, special_offer, building = ld["price"], ld["term"], ld["beds"], ld["baths"], ld["sq_ft"], ld["floor_num"], ld["available"], ld["special_offer"], ld["building"]
      available = "{:%B %d}".format(available).lower()
      
      formatted_listing += f"<li>{building + ' ' if building else ''}{beds} {pluralize(beds, 'bed')}, {baths} {pluralize(baths, 'bath')} on floor {floor_num} with {sq_ft} sf for {price}. Ready {available} with a {term}nth lease. {'' if not special_offer else f'{special_offer}!'}</li>"      
    
    formatted_listing += "</ul>"
      
  return formatted_listing[:-5]
  
def pluralize(num, word):
  return word if float(num) == 1 else f"{word}s"
  