from django import forms

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=30, widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput, required=False)