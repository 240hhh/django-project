from socket import fromshare
from .models import Register
from django import forms

class ReserverForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = {"reserver"}
        labels = {"reserver":"予約者"}
