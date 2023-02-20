from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .token import account_activation_token


# Create your views here.

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html', {'orders':orders})



@login_required  # bu decoratorni vazifasi , agar foydalanuvchi login qilib kirgan bo'lsagina  decorator ostidagi funksyalarni ishga tuahirishini ta'minlaydi
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():

            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        # print(user_form,'else')

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    # if request.dashboard.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data[
                                  'password'])  # Django'da cleaned_data['password'] funksiyasi foydalanuvchi parolini tekshirilgandan va tozalangandan keyin saqlashdir. Bu foydalanuvchi parolining xavfsizligini ta'minlash va ilova tomonidan o'rnatilgan talablarga javob berish uchun amalga oshiriladi.
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'dashboard': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):  # dashboard sign up qilgandan keyin , accountni activlashtiradigan funksya
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, dashboard.DoesNotExist):
    #     dashboard = None
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
