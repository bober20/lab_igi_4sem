from django import forms

from apps.cleaning_service_app.models import CustomUser, Client, Employee
from apps.users_app.custom_mixins import ValidationMixin


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telephone', 'age')


class ClientRegistrationForm(forms.ModelForm, ValidationMixin):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = Client
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(UserRegistrationForm().fields)
        self.order_fields(['email', 'first_name', 'last_name', 'age', 'telephone', 'password1', 'password2'])

    def clean(self):
        self.check_email(self.cleaned_data.get('email'))
        self.check_passwords(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))
        self.check_password_length(self.cleaned_data.get('password1'))
        self.check_age(self.cleaned_data.get('age'))
        self.check_telephone(self.cleaned_data.get('telephone'))


class EmployeeRegistrationForm(forms.ModelForm, ValidationMixin):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = Employee
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(UserRegistrationForm().fields)
        self.order_fields(['email', 'first_name', 'last_name', 'age', 'telephone', 'password1', 'password2'])

    def clean(self):
        self.check_email(self.cleaned_data.get('email'))
        self.check_passwords(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))
        self.check_password_length(self.cleaned_data.get('password1'))
        self.check_age(self.cleaned_data.get('age'))
        self.check_telephone(self.cleaned_data.get('telephone'))


class LoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
