from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import category,subCategory,product,Cart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from app.utils import Util
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import smart_str
from django.shortcuts import get_object_or_404

# Create your views here.
@csrf_exempt
@login_required
def home(request):
    cat = category.objects.all()
    pro = product.objects.all()
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategoryId')
        pro = product.objects.filter(subcategory=subcategory_id)
        return render(request,'category.html',{'products':pro}) 
    return render(request,'index.html',{'categories':cat,'products':pro}) 



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'User with the provided username or email already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        if user is not None:
            auth_login(request, user)
        return JsonResponse({'success': True})

   
    return render(request, 'login.html')  # Replace with your actual signup form template


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)

    return render(request, 'login.html')
    

def logout(request):
    auth_logout(request)
    return redirect('signup')

def contact(request):
    return render(request,'contact-us.html') 
def four04(request):
    return render(request,'404.html') 
def blog(request):
    return render(request,'blog.html') 
def blogsingle(request):
    return render(request,'blog-single.html') 
def shop(request):
    return render(request,'shop.html') 
def productDetails(request):
    return render(request,'product-details.html') 
def checkout(request):
    return render(request,'checkout.html') 
def cart(request):
    cart_products = Cart.objects.filter(user=request.user)
    for item in cart_products:
        item.total_price = item.product.price * item.quantity
    subtotal = sum(item.product.price * item.quantity for item in cart_products)
   
    percentage = (subtotal/100)*5
    total_bill = percentage + subtotal

    return render(request,'cart.html',{'cart_products':cart_products,'totalBill':subtotal,'per':percentage,'bill':total_bill}) 

@csrf_exempt
def resetPassword(request):
    email = request.POST.get('email')
    reset_link_base = 'http://127.0.0.1:8000/resetPasswordView'
    subject = 'Bizaibo Registration'
    template_path = 'EMAIL/reset_email.html'

    if not email:
        return JsonResponse({'status': 'failed', 'status_code': 400, 'message': 'Email is required.', 'data': {}})
    if not User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'failed', 'status_code': 404, 'message': 'Invalid Email', 'data': {}})
    
    user = User.objects.get(email=email)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.id).encode())

    reset_link = f'{reset_link_base}/{uid}/{token}'
    context = {'reset_link': reset_link, 'email': email}

    try:
        print('==============================>',reset_link)
        # Util.send_email(subject, template_path, context, email)
        return JsonResponse({'status': 'success', 'status_code': 200, 'message': 'Email sent successfully.', 'data': {}})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'status_code': 400, 'message': 'Failed to send reset email.', 'data': {}})
    
def resetPasswordView(request, uid, token):
    if request.method == 'POST':
        try:
            uid_decoded = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=uid_decoded)

            if default_token_generator.check_token(user, token):
                password = request.POST.get('password')
                if password:
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    return JsonResponse({'status': 'success', 'message': 'Password reset successful.'})
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Password is required.'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Invalid token.'})
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({'status': 'failed', 'message': 'Password reset not successful.'})
    else:
        return render(request, 'resetPasswordChange.html', {'uid': uid, 'token': token})

@login_required
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        Product = get_object_or_404(product, id=product_id)

        
        # Check if the cart item already exists for this user and product
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=Product)
        
        if not created:
            # If the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
        else:
            # If it's a new item in the cart, set the initial quantity to 1
            cart_item.quantity = 1
        
        cart_item.save()
        
        return JsonResponse({'message': 'Product added to cart'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_cart_quantity(request):
    print('-=-=-=-=-=-=-=>',request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()
            cart_products = Cart.objects.filter(user=request.user)
            
            subtotal = sum(item.product.price * item.quantity for item in cart_products)
            percentage = (subtotal/100)*5
            total_bill = percentage + subtotal

            return JsonResponse({'message': 'Cart updated', 'quantity': cart_item.quantity, 'total_price': cart_item.product.price * cart_item.quantity,'sub_total':subtotal,'per':percentage,'bill':total_bill}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart item not found'}, status=404)

    return JsonResponse({'message': 'Invalid request'}, status=400)