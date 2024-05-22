from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', White_View, name='home'),
    path('home/', Home_View, name='home'),
    path('shop', Shop_View, name='shop'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('cart', cart, name='cart'),
    path('product/<int:product_id>/', productdetail, name='product_detail'),
    path('login', Log_in, name='login'),
    path('signup', Sign_up, name='signup'),
    path('detail', productdetail, name='detail' ),
    path('checkout', checkout, name='checkout'),
    path('placeorder', placeorder, name='placeorder'),
    path('vote/<int:vote>/<int:product_id>/', vote, name='vote'),
    path('add-comment/<int:product_id>', addcomment, name='addcomment'),
    path('favorite', favorite, name='favorite'),
    path('addfavorite/<int:product_id>', addfavorite, name='addfavorite'),
    path('thankyou', Thank_You,name='thankyou'),
]