from django.shortcuts import render, redirect
from Authentication.forms import RegistrationForm, PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from Authentication.utils import send_activation_email, send_reset_password_email
from Authentication.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from MainApp.models import Customer
from MainApp.forms import CustomerProfileForm
from django.views import View

# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):

    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('home')
        elif request.user.is_customer:
            return redirect('home')
        return redirect('home')

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both Fields are required .')
            return redirect('login')
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password ')
            return redirect('login')
        if not user.is_active:
            messages.error(
                request, 'Your Account is inactive. Please aactive your account.')
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_seller:
                return redirect('home')
            elif request.user.is_customer:
                return redirect('home')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password ')
            return redirect('login')
    return render(request, 'Authentication/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse(
                'activate', kwargs={'uidb64': uidb64, 'token': token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email, activation_url)

            messages.success(
                request, 'Registration successfully ! Please check your email to activate your account'
            )
            return redirect('login')

    else:
        form = RegistrationForm()
    return render(request, 'Authentication/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.warning(
                request, 'This account has been alredy activated.')
            return redirect('login')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, 'Your account has been activated successfully !')
            return redirect('login')
        else:
            messages.error(
                request, 'The activation link is invalid or has expired .')
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link .')
        return redirect('login')


def pasword_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={
                                    'uidb64': uidb64, 'token': token})
                absolute_reset_url = request.build_absolute_uri(reset_url)

                send_reset_password_email(user.email, absolute_reset_url)
                messages.success(
                    request, ('We have sent you a password reset link . Please check your email.'))
                # print('sendLink')
                return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'Authentication/password_reset.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.success(
                request, 'This link has expired or is invalid .')
            return redirect('password_reset')
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.error(
                    request, 'Your password has been successfully reset.')
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form = SetPasswordForm(user)
        return render(request, 'Authentication/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'An error occured. Please try again later.')
        return redirect('password_reset')


class ProfileView(View):
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm()

        return render(request, 'Authentication/profile.html', {'form': form})

    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(
                request.POST, request.FILES, instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            customer = form.save(commit=False)

            # DEBUG: Check if avatar is present
            #print("Avatar uploaded: ", request.FILES.get('avatar'))

            customer.user = request.user
            customer.save()
            messages.success(
                request, 'Congratulations! Your profile has been updated.')
            return redirect('profile')

        return render(request, 'Authentication/profile.html', {'form': form})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'Authentication/address.html', {'address': add})
