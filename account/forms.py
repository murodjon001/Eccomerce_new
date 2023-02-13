
from django import forms
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter username', min_length=1, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',error_messages={'reuquired': "Sorry you will need an email"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_user_name(self):  # usernameni databasada bor yo'qligini tekshiradi
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            print(r)
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():  # Ushbu kod berilgan elektron pochta manziliga ega foydalanuvchi foydalanuvchi bazasida allaqachon mavjudligini tekshiradi.
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # super funksya classning barcha atribulariga kirish imkonini beradi
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))  #  Ushbu(attrs kod HTML-da foydalanuvchi nomi uchun sinf, to'ldiruvchi va identifikator kabi maxsus atributlarga ega bo'lgan kirish maydonini yaratadi.
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(forms.ModelForm):

    """Eslatma!
         Label kodi - mahsulotlarni aniqlash va inventarni kuzatish uchun ishlatiladigan shtrix-kod turi. U odatda narx, o'lcham va vazn kabi mahsulot
         ma'lumotlarini, shuningdek, buyum uchun noyob identifikatorni o'z ichiga oladi. Yorliq kodlari odatda chakana savdo do'konlarida kassadagi
          narsalarni tezda skanerlash va zaxiralar darajasini kuzatish uchun ishlatiladi."""

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Firstname', min_length=1, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    class Meta:  # bu class databazadagi ma'lumotlarni o'zgartirib beradi
        model = UserBase
        fields = ('email', 'first_name',)

    def __init__(self, *args, **kwargs):
        """Ushbu kod Django Form sinfidan meros bo'lgan shakl sinfini o'zgartirmoqda. Shakl to'g'ri bo'lishi uchun
           "user_name" va "email" maydonlarini talab qiladi."""

        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}
    ))

    def clean_email(self):
        email= self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise  forms.ValidationError(
                "Bunday email adress ma'lumotlar omborida yo'q"
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
