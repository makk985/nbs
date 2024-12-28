from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import UserProfile, SellerProfile, BuyerProfile
from django.contrib.auth.decorators import login_required
from products.models import Product
from.models import UserCart
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def index(request):
    #check if user is logged in
    context={
        'is_authenticated': request.user.is_authenticated,
        'user':request.user,
        'is_seller': False
    }
    if request.user.is_authenticated:
        try:
            # Check if the user has a seller profile
            seller_profile = request.user.userprofile.sellerprofile
            context['is_seller'] = True
        except:
            context['is_seller'] = False
    return render(request, 'index.html',context)

def signup(request):
    if request.method=='POST':
        # Get form values
        
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists')
                return redirect('signup')

            user=User.objects.create_user( username=email,first_name=first_name, last_name=last_name, email=email, password=password)
            buyer_profile = BuyerProfile.objects.create(
                user_profile=user.userprofile,
                
            )

            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login') 

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html')

@csrf_exempt # to avoid csrf protection for post request to google
def google_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_token_str = data.get('id_token')
        if id_token_str:
            try:
                # Verify the ID token
                idinfo = id_token.verify_token(id_token_str, requests.Request(), settings.GOOGLE_CLIENT_ID)

                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError('Wrong issuer.')
                # Get the user's Google ID and email
                user_id = idinfo['sub']
                email = idinfo['email']
                name = idinfo['name']

                # Check if the user already exists
                try:
                    user = User.objects.get(username=email)
                except User.DoesNotExist:
                    # Create new user.
                    user = User.objects.create_user(username = email, password= user_id, email=email, first_name=name )
                user = authenticate(username=email, password=user_id)
                login(request, user)
                return JsonResponse({'success':True}, status=200)


            except ValueError as e:
                # Invalid token
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error':'No id token provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def login_view(request):
    if request.method=='POST':
        email=request.POST.get('email') 
        password=request.POST.get('password')       

        #authenticate user
       
        user=authenticate(request, username=email, password=password)
        

        if user is not None:
            auth_login(request,user)
            messages.success(request, 'Login successful!')
            return redirect('index')  # Replace 'home' with your home page URL name
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    
    return render(request, 'login.html')

def logout_view(request):
    # Clear all existing messages
    storage = get_messages(request)
    storage.used = True
    #perform logout
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('index')  

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return redirect('login')

def seller_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        business_name = request.POST.get('business_name')
        business_address = request.POST.get('business_address')

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists')
                return redirect('seller_signup')

            # Create user and profiles
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            
            # sellerProfile is created  
            seller_profile = SellerProfile.objects.create(
                user_profile=user.userprofile,
                business_name=business_name,
                business_address=business_address
            )
            
            messages.success(request, f'Seller account created successfully! Your Seller ID is: {seller_profile.seller_account_id}')
            return redirect('seller_login')

        except Exception as e:
            messages.error(request, f'Error creating seller account: {str(e)}')
            return redirect('seller_signup')

    return render(request, 'seller_signup.html')

def seller_login(request):
    if request.method == 'POST':
        seller_id = request.POST.get('seller_id')
        password = request.POST.get('password')

        try:
            # Find the seller profile
            seller_profile = SellerProfile.objects.get(seller_account_id=seller_id)
            user = seller_profile.user_profile.user
            
            # Authenticate using email and password
            user = authenticate(request, username=user.email, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('seller_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except SellerProfile.DoesNotExist:
            messages.error(request, 'Invalid Seller ID')
        
        return redirect('seller_login')

    return render(request, 'seller_login.html')

def seller_logout(request):
    storage = get_messages(request)
    storage.used = True
    #perform logout
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('index')

def add_product(request):
    return render(request, 'add_product.html')
@login_required
def seller_dashboard(request):
    try:
        seller_profile = request.user.userprofile.sellerprofile
        context = {
            'seller': seller_profile,
            'user': request.user
        }
        return render(request, 'seller_dashboard.html', context)
    except SellerProfile.DoesNotExist:
        messages.error(request, 'Seller profile not found')
        return redirect('index')

@login_required
def add_to_cart(request, product_id):
       product = Product.objects.get(id=product_id)
       cart_item, created = UserCart.objects.get_or_create(user=request.user, product=product)
       if not created:
           cart_item.quantity += 1  # Increase quantity if already in cart
           cart_item.save()
       return redirect('my_cart')  # Redirect to cart

@login_required
def remove_from_cart(request, product_id):
    cart_item = UserCart.objects.get(user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('my_cart')  # Redirect to cart view

@login_required
def my_cart(request):
    cart_items = UserCart.objects.filter(user=request.user)
    return render(request, 'UserCart.html', {'cart_items': cart_items, 'user': request.user, 'is_authenticated': request.user.is_authenticated})









