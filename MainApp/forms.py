from django import forms
from MainApp.models import Customer
from MainApp.models import Contact
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fname', 'mname', 'lname', 'address', 'gender', 'date_of_birth',
                  'phone', 'city', 'state', 'district', 'avatar']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'mname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional Middle Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Choose Image'}),
        }
        labels = {
            'fname': 'First Name',
            'mname': 'Middle Name',
            'lname': 'Last Name',
            'address': 'Address',
            'gender': 'Gender',
            'DoB': 'Date of Birth',
            'phone': 'Phone Number',
            'city': 'City',
            'state': 'State',
            'district': 'District',
            'avatar': 'Profile Image',
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'gmail', 'phone_number', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }