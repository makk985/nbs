from django.shortcuts import render, redirect
from .models import Product
from django.db.models import Q #for searching complex queries




# Create your views here.
def add_product(request):
    if request.method=='POST':

        #creating product instance
        product=Product(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            quantity=request.POST.get('quantity'),
            image=request.FILES.get('image')
        )
        product.save()
        return redirect('seller_dashboard')

    

    return render(request, 'seller_dashboard.html')

def seller_dashboard(request):
    products=Product.objects.all() #fetching all products
    context={
        'products':products
    }
    
    return render(request, 'seller_dashboard.html',context)

def delete_product(request, id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('seller_dashboard')


def search_results(request):
    query=request.GET.get('q')
    products=Product.objects.all()
    

    if query:
        products=products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        

    context={
         'products': products,
        'query': query,
        'is_authenticated': request.user.is_authenticated,  # Check if user is authenticated
        'is_seller': False,  # Check if user is a seller
        'user': request.user  # Pass the user object
    }
    
    return render (request,'search_results.html',context)