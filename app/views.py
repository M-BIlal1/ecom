from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import category,subCategory,product,Cart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from app.models import Profile

@csrf_exempt
def home(request):
    cat = category.objects.all()
    pro = product.objects.all()
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        pro = product.objects.filter(category_id=cat_id)
        homeProduct = render_to_string('homeProduct.html',{'products':pro})
        return JsonResponse({
            'status':'sucess',
            'message':'get product by category successfully',
            'data':homeProduct
        })
    return render(request,'index.html',{'categories':cat,'products':pro}) 


@csrf_exempt
def signup(request):

    if request.method == 'POST':
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            email = request.POST.get("email")
            city = request.POST.get("city")     
            gender = request.POST.get("gender")
            country = request.POST.get("country")
            password = request.POST.get("password")
            confirm_password = request.POST.get("password_repeat")
            username = first_name + last_name           

            if password != confirm_password:
                return JsonResponse({'success': False, 'error': 'Passwords do not match'}, status=400)

            if  User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'User with the provided  email already exists'}, status=400)

            user = User.objects.create_user(
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        username = username 
                    )
            user.save()
            if gender == "Male":
                gender = 'M'
            else:
                gender = 'F'    
            profile = Profile.objects.create(
                user=user,
                gender=gender,
                city=city,
                country=country
            )
    # No need to call profile.save() because create() already saves the instance

            
            if user is not None:
                auth_login(request, user)
            return JsonResponse({
                        'status': 'success',
                        'status_code': 201,
                        'message': 'Registration Successful',
                        'data': {'user_id': user.id}
                    }, status=201)
        except Exception as e:
            return JsonResponse({
                        'status': 'fail',
                        'status_code': 500,
                        'message': f'Registration UnSuccessful,{str(e)}',
                        'data': {}
                    }, status=201)

   
    return render(request, 'register.html')  # Replace with your actual signup form template

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # user = authenticate(request,username=email, password=password)
        
        user = User.objects.get(Q(username=email) | Q(email=email))
        if user is not None:
            if user.check_password(password):
                auth_login(request, user)
                return JsonResponse({
                            'status': 'success',
                            'status_code': 201,
                            'message': 'Sign in Successful',
                            'data': {'user_id': user.id}
                        }, status=201)
                
        
            else:
                 return JsonResponse({
                        'status': 'fail',
                        'status_code': 400,
                        'message': 'Invalid Credentials',
                        'data': {}
                    }, status=201)
        else:
            return JsonResponse({
                        'status': 'fail',
                        'status_code': 400,
                        'message': 'Invalid Credentials',
                        'data': {}
                    }, status=201)


    return render(request, 'signin.html')
    

def logout(request):
    auth_logout(request)
    return redirect('signin')

def contact(request):
    return render(request,'contact-us.html') 
def four04(request):
    return render(request,'404.html') 
def placeorder(request):
    return render(request,'place-order.html') 
def blogsingle(request):
    
    return render(request,'resetPassword.html') 

@csrf_exempt
@login_required
def store(request):
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        min_value = request.POST.get('min_value')
        max_value = request.POST.get('max_value')
        if cat_id:
            pro = product.objects.filter(category_id=cat_id)
        else:
            pro = product.objects.filter(price__gte=min_value, price__lte=max_value)
        
        storeProduct = render_to_string('storeProducts.html',{'product':pro})
        return JsonResponse({
            'status':'sucess',
            'message':'get storeProduct by category successfully',
            'data':storeProduct
        })
    cat = category.objects.all()
    pro = product.objects.all()
    cart_items = Cart.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request,'store.html',{'product':pro,'cart':cart_items,'categories':cat}) 

@login_required
def getProduct(request,pid):
    request.session['pid'] = pid
        
    return redirect('productDetail')
@login_required
def productDetails(request):
    pid = request.session.get('pid')
    pro = product.objects.get(pk=pid)
    return render(request,'product-detail.html',{'product':pro}) 

def checkout(request):
    return render(request,'checkout.html') 

def cart(request):
    cart_products = Cart.objects.filter(user=request.user)
    for item in cart_products:
        item.total_price = item.product.price * item.quantity
    subtotal = sum(item.product.price * item.quantity for item in cart_products)
   
    percentage = (subtotal/100)*5
    total_bill = percentage + subtotal

    return render(request,'cart.html',{'cart':cart_products,'totalPrice':subtotal,'tax':percentage,'totalBill':total_bill}) 

@csrf_exempt
def reset(request):
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
        # Util.send_email(subject, template_path, context, email)
        return JsonResponse({'status': 'success', 'status_code': 200, 'message': 'Email sent successfully.', 'data': {}})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'status_code': 400, 'message': 'Failed to send reset email.', 'data': {}})
    
def resetPasswordView(request, uid, token):
   
    try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        
        return redirect('resetPassword')
    else:
        # return JsonResponse({'status': 'failed', 'message': 'Password reset not successful.'})
        return redirect('signin')
               
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return JsonResponse({'status': 'Success', 'message': 'Password reset  successful.'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Password reset not successful.'})
    
    return render(request, 'resetPassword.html')


@login_required
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')
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
        pro = product.objects.all()
        cart_items = Cart.objects.filter(user=request.user).values_list('product_id', flat=True)    
        cart_display_html = render_to_string('storeProducts.html', {'product':pro,'cart':cart_items})
        # return render('cartProduct.html',{'cart':cart_products})
        return JsonResponse({
                            'status': 'success',
                            'status_code': 200,
                            'message': 'Product added to cart',
                            'cart_display': cart_display_html,
                            'cart':len(cart_items)
                        })
        
    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_cart_quantity(request):

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

@csrf_exempt
def removeCart(request):
    prod_id = request.POST.get('cartProductId')
    pro = Cart.objects.get(product_id=prod_id,user=request.user)
    pro.delete()
    cart_products = Cart.objects.filter(user=request.user)
    for item in cart_products:
        item.total_price = item.product.price * item.quantity
    cart_display_html = render_to_string('cartProduct.html', {'cart': cart_products})
    subtotal = sum(item.product.price * item.quantity for item in cart_products)
    percentage = (subtotal/100)*5
    total_bill = percentage + subtotal
    # return render('cartProduct.html',{'cart':cart_products})
    return JsonResponse({
                        'status': 'success',
                        'status_code': 200,
                        'message': 'product remove from cart ',
                        'cart_display': cart_display_html,'sub_total':subtotal,'per':percentage,'bill':total_bill,'cart':len(cart_products)
                    })

