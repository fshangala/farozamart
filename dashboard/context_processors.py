from dashboard.function import getOptions

def siteOptionsContext(request):
  return {'options':getOptions()}