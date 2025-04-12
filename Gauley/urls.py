"""
URL configuration for Gauley project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MainApp import urls as MainApp_urls
from Authentication import urls as Authentication_urls
from PaymentGateway import urls as PaymentGateway_urls
from RatingAndReview import urls as RatingReview_urls
from Blog import urls as Blog_urls
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    
    path('admin/', admin.site.urls),
    path('', include(MainApp_urls)),
    path('authentication/', include(Authentication_urls)),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('paymentgateway/',include(PaymentGateway_urls)),
    path('Blog/',include(Blog_urls)),
    path('RatingReview/',include(RatingReview_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
