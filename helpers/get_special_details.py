import re

def get_special_details(apartment):
  special_offer_div = apartment.find("div", class_="special-offer")
  
  if not special_offer_div:
    return ""
  
  match = re.compile(r'popover="[^"]*"').findall(str(special_offer_div.encode_contents()))
  
  return re.sub(" select apartment homes| on select apartment homes", "", match[0].replace("popover=", "")[1:-1])
  