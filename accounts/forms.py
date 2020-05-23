from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField

from .models import CongoUser, CongoUserProfile


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CongoUser
        fields = ['phone_number', ]


class PasswordSettingForm(UserCreationForm):
    class Meta:
        model = CongoUser
        fields = ['password1', 'password2', ]


class LoginForm(forms.Form):
    phone_number = PhoneNumberField(label='Phone Number')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if not user:
                raise forms.ValidationError(
                    'This phone number does not exists')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This account is not active')
            return super(LoginForm, self).clean()


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CongoUserProfile
        fields = ['first_name',
                  'last_name',
                  'business_name',
                  'gst_number',
                  'business_type',
                  'business_category']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'business_name': 'Business Name',
            'gst_number': 'GST Number',
            'business_type': 'Business Type',
            'business_category': 'Business Category',
        }
