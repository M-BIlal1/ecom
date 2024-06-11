from django.urls import path,include
from app import views
urlpatterns = [
path('', views.signup),
path('home', views.home, name='home'),
path('logout', views.logout, name='logout'),
path('register', views.signup, name='register'),
path('signin', views.login, name='signin'),
path('contact', views.contact, name='contact'),
path('four04', views.four04, name='four04'),
path('place-order', views.placeorder, name='place-order'),
path('blogsingle', views.blogsingle, name='blogsingle'),
path('store', views.shop, name='shop'),
path('product-detail', views.productDetails, name='product-details'),
path('checkout', views.checkout, name='checkout'),
path('cart', views.cart, name='cart'),
path('reset', views.resetPassword, name='resetPasswordCahnge'),
path('resetPasswordView/<str:uid>/<str:token>/', views.resetPasswordView, name='resetPasswordChange'),
path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),



]

