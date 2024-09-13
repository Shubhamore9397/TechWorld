
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HOME, name='home' ),
    path('base/', views.BASE, name='base' ),
    path('products/', views.PRODUCT, name='products' ),
    path('search/',views.SEARCH, name='search'),
    path('product_details/<pid>', views.PRODUCT_DETAILS, name='product_details'),
    path('contact/',views.CONTACT, name='contact'),
    path('register/',views.REGISTER, name='register'),
    path('login/',views.LOGIN, name='login'),
    path('logout/',views.LOGOUT, name='logout'),
    
    # For Cart Functionality
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('cart/checkout/',views.CHECKOUT,name='checkout'),
    

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)