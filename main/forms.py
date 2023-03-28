from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class EditDetails(forms.Form):
    status = forms.BooleanField(required=False, label="bleh")
    start_date = forms.DateField(label="Start Date", required=False, widget=AdminDateWidget())