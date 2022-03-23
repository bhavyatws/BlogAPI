from django.contrib.auth.forms import UserCreationForm
from . models import  User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.core import validators
import re

def email_validator(value):
    print(value)
    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(pattern,value):
        print("Valid email id")
    else:
        print("Invalid email id")
        raise forms.ValidationError("Enter valid email")
   
        
   
        

# validators=[email_validator]
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email',validators=[email_validator],widget=forms.TextInput(

        attrs={'auto_focus': True, 'class': 'form-control',

               'placeholder': 'Enter Username or Email',



               }))
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current_password',
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )


# Creating Form for Registration
# from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
           
        }
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        
        
        

# class CommentForm(forms.Form):
#     comment = forms.CharField(widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter Comment here',
#         'cols': '5',
#         'rows': '3'

#     }))
#     post_id = forms.CharField(widget=forms.HiddenInput())
#     parent_Sno = forms.CharField(widget=forms.HiddenInput())


# class ReplyCommentForm(forms.Form):
#     reply = forms.CharField(widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter Comment here',
#         'cols': '5',
#         'rows': '3'

#     }))
