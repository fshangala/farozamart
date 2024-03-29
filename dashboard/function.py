from dashboard import models
from django.core.mail import send_mail

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

def admin_send_mail(subject:str,message:str,receipients:list):
  options = getOptions()
  if options.get('mailing_status') == 'ACTIVATED':
    send_mail(
      subject=subject,
      message=message,
      from_email=options['site_mail'],
      recipient_list=receipients
    )