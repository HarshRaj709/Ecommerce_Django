from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import EmailValidator
from .models import Extrainfo,Contact

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    first = forms.CharField(max_length=30, required=False)
    last = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Accept the user instance when the form is instantiated
        super().__init__(*args, **kwargs)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Only check if the username is different from the current user's username
        if username != self.user.username:  # Compare new value with the current value
            if User.objects.filter(username=username).exists():
                raise ValidationError('Username is already taken, please choose a different one.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Only check if the email is different from the current user's email
        if email != self.user.email:  # Compare new value with the current value
            if User.objects.filter(email=email).exists():
                raise ValidationError('This email is already registered, please choose another.')
        return email

    def save(self, user):
        if self.user is None:
            raise ValueError("User instance is required for saving.")
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first']
        user.last_name = self.cleaned_data['last']
        user.email = self.cleaned_data['email']
        user.save()

class Extraform(forms.ModelForm):
    class Meta:
        model = Extrainfo
        fields = ['state','country','Address','contact_no','zip']           #converted contact field to CharField to use isdigit()

    def clean_contact_no(self):
        contact = self.cleaned_data.get('contact_no')
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit phone number.')
        return contact
    
    def clean_zip(self):
        zip = str(self.cleaned_data['zip'])
        if not zip.isdigit() or len(zip)!=6:
            raise forms.ValidationError('Please Enter Valid Zip address')
        return zip
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['description']
