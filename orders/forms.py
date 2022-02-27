from django import forms
from .models import Order, AllFrom


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


class AFrom(forms.ModelForm):
    class Meta:
        model = AllFrom
        fields = '__all__'
    # number = forms.IntegerField(label='Число')

