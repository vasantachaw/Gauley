from django.urls import path
from PaymentGateway.views import checkout, orders
from django.conf import settings
from django.conf.urls.static import static
from PaymentGateway import views
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders, name='order'),
    path('paymentsdone/', views.payment_done, name='paymentdone'),

    path('integrate/', views.integrate, name='integrate'),
    path('khalti_payment/', views.khalti_payment, name='khalti_payment'),
    path('submit_khalti_payment/', views.submit_khalti_payment,
         name='submit_khalti_payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
