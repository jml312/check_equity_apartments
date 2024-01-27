def get_building(text_data, multi_options):
  building = None
  if len(multi_options) != 0:
    for text in text_data:
      for name in multi_options:
        if name in text.lower():
          building = ''.join((x for x in name if not x.isdigit()))
  return {
    "building": capitalize(building)
  }
  
def capitalize(word):
  if not word: 
    return None
  return word[0].upper() + word[1:]