from django import forms
from dashboard.function import saveOption
from dropshipping import models
from store.models import Order

class SteadfastConfiguration(forms.Form):
  steadfast_status=forms.ChoiceField(choices=(('ACTIVATED','Activated'),('DEACTIVATED','Deactivated')), widget=forms.Select(attrs={'class':'form-control'}))
  steadfast_api_key=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  steadfast_api_secrete=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  steadfast_delivery_charge=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  
  def save(self):
    for x in ['steadfast_status','steadfast_api_key','steadfast_api_secrete','steadfast_delivery_charge']:
      saveOption(x,self.cleaned_data[x])

class SteadfastCreateDeliveryOrder(forms.Form):
  order=forms.ModelChoiceField(queryset=Order.objects.none(),widget=forms.Select(attrs={'class':'form-control'}))
  
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.options=getOptions()
  
  def clean(self):
    cleaned_data = super().clean()
    
    if self.options.get('steadfast_api_key') and self.options.get('steadfast_api_secrete'):
      self.add_error(error='Unable to make automatic delivery')
      
    return cleaned_data
  
  def save(self):
    order = self.cleaned_data['order']
    header={
      'Api-Key':option.get('steadfast_api_key'),
      'Api-Secrete':option.get('steadfast_api_secrete'),
      'Content-Type':'application/json'
    }
    data={
      'invoice':order.id,
      'recipient_name':order.user.profile.full_name(),
      'recipient_phone':order.user.profile.phone,
      'recipient_address':order.user.profile.address,
      'cod_amount':0
    }
    response = requests.post(settings.STEADFAST_BASEURL+'/create-order',data=data,header=header)
    if response.status_code == 200:
      resulte = response.json()
      models.SteadFastDelivery.objects.create(
        consignment_id=resulte['consignment_id'],
        invoice=resulte['invoice'],
        tracking_code=resulte['tracking_code'],
        created_at=resulte['created_at'],
        updated_at=resulte['updated_at']
      )