from django import forms
from phone_field import PhoneField
from django.core.validators import RegexValidator
   
class TokenRequestForm(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        super(TokenRequestForm, self).__init__(*args, **kwargs)
        self.fields['book_for'] = forms.ChoiceField(label="Book For",help_text='Select the date for which you want an appointment',choices=choices, widget=forms.Select(), required=True)
        self.fields['p_name'] = forms.CharField(label='Name', help_text='Enter your full name')
        self.fields['p_number'] = forms.CharField(label='Phone number', help_text='Enter your phone number', max_length=10, validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')])
