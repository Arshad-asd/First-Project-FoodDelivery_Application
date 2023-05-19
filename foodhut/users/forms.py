from django import forms
from django.contrib.auth.models import User
from users.models import CustomUser
class Aforms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['name','mobile','email','password']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True, attrs={'class':'form-control'}),
        } 
