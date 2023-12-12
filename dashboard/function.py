from dashboard import models

def getOptions():
  options = models.Option.objects.all()
  options_dict = dict()
  for option in options:
    options_dict[option.name] = option.value
  
  return options_dict

def saveOption(name,value):
  try:
    option = models.Option.objects.get(name=name)
  except Exception as e:
    models.Option.objects.create(name=name,value=value)
  else:
    option.value = value
    option.save()