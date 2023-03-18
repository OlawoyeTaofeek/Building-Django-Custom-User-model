# There are diifferent ways of creating Authentication forms

# LOGIN
# 1. Django inbuilt one : for login we will be using AuthenticationForm 
# 2. And a custom one created by inheriting from forms.ModelForm  

# REGISTRATION
# 1. Django inbuilt approach: Using UserCreationForm
# 2. And a custom one created by inheriting from forms.ModelForm  


from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationForm(forms.ModelForm):

    password_1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password_1', 'password_2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists:
            raise forms.ValidationError("email is taken")
        return email
    
    def clean_password(self):
        cleaned_data = super().clean()
        
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')
        if password_1 is not None and password_1 != password_2:
            self.add_error('Password does not match')
        return cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.password_1 = self.cleaned_data['password_1']
        user.password_2 = self.cleaned_data['password_2']
        if commit:
            user.save()
        return user



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password_1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 is not None and password_1 != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



