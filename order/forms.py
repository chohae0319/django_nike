from django import forms
from .models import Shipping

class ShippingForm(forms.ModelForm):

    class Meta:
        model = Shipping
        fields = ['destination_nickname',
                  'receiver', 'receiver_phone', 'receiver_address']


