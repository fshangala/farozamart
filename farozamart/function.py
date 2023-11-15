from farozamart import models

def getOptions()->dict[str,str]:
  options = models.Option.objects.all()
  options_dict = dict()
  for option in options:
    option_dict[option.name] = option.value
  
  return option_dict