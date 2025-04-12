from django.urls import path
from MainApp import views
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from MainApp.views import add_to_cart
from MainApp.views import minus_cart, vegs
from MainApp.views import plus_cart
from MainApp.views import show_cart, ProductDetailsView
from MainApp.views import remove_cart, emptyCart
from MainApp.views import beverage, proteins
from MainApp.views import instantfood, dairy
from MainApp.views import pickle, fruits, grocery
from MainApp.views import wishList,contact
from MainApp.views import ToggleWishListView
from MainApp.views import buy_now
from MainApp.views import priceFilter
from MainApp.views import price_filter_all_product
from MainApp.views import das,product_search,product_autocomplete
urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', show_cart, name='show_cart'),
    path('pluscart/', plus_cart),

    path('minuscart/', minus_cart),
    path('removecart/', remove_cart),
    path('product-detail/<int:pk>',
         ProductDetailsView.as_view(), name='product_detail'),
    path('emptycart/', emptyCart, name='emptycart'),
    path('wishlist/toggle/<int:pk>',
         ToggleWishListView.as_view(), name='toggle_wishlist'),
    path('buy_now/<int:pk>/', buy_now, name='buy_now'),
    # ------------------------------fil;tering products by category------------------

    path('vegetables/', vegs, name='vegetables'),
    path('beverage/', beverage, name='beverage'),
    path('proteins/', proteins, name='proteins'),
    path('instantfoods/', instantfood, name='instantfood'),
    path('dairy/', dairy, name='dairy'),
    path('pickleAndjam/', pickle, name='pickleAndJam'),
    path('fruits/', fruits, name='fruits'),
    path('grocery/', grocery, name='grocery'),
    path('Wishlist/', wishList, name='wishlist'),
    path('pricefilter/<slug:category_slug>/',priceFilter,name='filter'),
    path('pricefilter_all_product/',price_filter_all_product,name='allfilter'),
    path('das/',das,name='das'),
     path('search/', product_search, name='product_search'),
     path('autocomplete/', product_autocomplete, name='product_autocomplete'),
     path('contact/',contact,name='contact'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
