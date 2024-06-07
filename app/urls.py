from django.urls import path,include
from app import views
urlpatterns = [
path('', views.signup),
path('home', views.home, name='home'),
path('logout', views.logout, name='logout'),
path('signup', views.signup, name='signup'),
path('login', views.login, name='login'),
path('contact', views.contact, name='contact'),
path('four04', views.four04, name='four04'),
path('blog', views.blog, name='blog'),
path('blogsingle', views.blogsingle, name='blogsingle'),
path('shop', views.shop, name='shop'),
path('productDetails', views.productDetails, name='product-details'),
path('checkout', views.checkout, name='checkout'),
path('cart', views.cart, name='cart'),
path('reset', views.resetPassword, name='resetPasswordCahnge'),
path('resetPasswordView/<str:uid>/<str:token>/', views.resetPasswordView, name='resetPasswordChange'),



]

