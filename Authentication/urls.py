from django.urls import path
from Authentication.views import register_view
from Authentication.views import activate_account
from Authentication.views import password_reset_confirm_view
from Authentication.views import pasword_reset_view
from Authentication.views import login_view, ProfileView, address
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static
from Authentication.forms import MyPasswordChangeForm

urlpatterns = [

    path('login/', login_view, name='login'),

    path('register/', register_view, name='register'),
    path('activate/<str:uidb64>/<str:token>/',
         activate_account, name='activate'),
    path('password_reset/', pasword_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         password_reset_confirm_view, name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('passwordchange/', PasswordChangeView.as_view(
         template_name='Authentication/changepassword.html',
         success_url='/authentication/profile/',
         form_class=MyPasswordChangeForm
         ), name='changepassword'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
