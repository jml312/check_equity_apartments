from datetime import datetime

def get_apartment_details(text_data, apartment_criteria):
  try:
    price = text_data[0].replace("\n\n", "")
    term = (f"{text_data[1]} {text_data[2]}").replace("\n\n\r\n", "")
    beds = text_data[3]
    baths = text_data[6]
    sq_ft = text_data[8].replace("\n\n", "")
    floor_num = text_data[11].replace("\n\n\r\n", "")

    month, day, year = list(map(int, text_data[13].replace("\r\n", "").split("/")))
    available_date = datetime(year, month, day)
    
    meets_price = meets_criteria(int(price.replace(",", "").replace("$", "")), "price", apartment_criteria)
    meets_term = meets_criteria(int(term.split(" ")[0]), "term", apartment_criteria)
    meets_beds = meets_criteria(float(beds), "beds", apartment_criteria)
    meets_baths = meets_criteria(float(baths), "baths", apartment_criteria)
    meets_sq_ft = meets_criteria(int(sq_ft), "sq_ft", apartment_criteria)
    meets_floor_num = meets_criteria(int(floor_num), "floor_num", apartment_criteria)
    meets_available_date = meets_criteria(available_date, "availability", apartment_criteria)
    
    if not all([meets_price, meets_term, meets_beds, meets_baths, meets_sq_ft, meets_floor_num, meets_available_date]):
      return False, ""

    return True, {
      "price": price,
      "term": term,
      "beds": beds,
      "baths": baths,
      "sq_ft": sq_ft,
      "floor_num": floor_num,
      "available": available_date
    }
  except Exception:
    return False, ""

def meets_criteria(data, key, apartment_criteria):
  has_min = bool(apartment_criteria[key]["min"])
  has_max = bool(apartment_criteria[key]["max"])

  if not has_min and not has_max:
    return True
  elif has_min and not has_max:
    return apartment_criteria[key]["min"] <= data
  elif not has_min and has_max:
    return apartment_criteria[key]["max"] >= data
  else:
    return apartment_criteria[key]["min"] <= data and apartment_criteria[key]["max"] >= data