from django.db.models import Count,Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart,Payment,OrderPlaced
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay



# Create your views here.


class home(View):
    def get(request):
     totalitem = 0
     if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
     return render(request,"app/home.html",locals())


@login_required
def about(req):
    totalitem= 0
    wishitem=0
    if req.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=req.user))
    return render(req,"app/about.html",locals())

@login_required
def contact(req):
    totalitem= 0
    wishitem=0
    if req.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=req.user))
    return render(req,"app/contact.html",locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem= 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         product = Product.objects.filter(category=val)
         title = Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title') 
        totalitem= 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/category.html',locals())   
     
class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW') 
        bottomwears = Product.objects.filter(category='BW')     
        mobiles = Product.objects.filter(category='M') 
        laptop = Product.objects.filter(category='L')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))   
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptop':laptop})
        
        

class ProductDetails(View):
    def get(self,request,pk):
        totalitem=0
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/productdetail.html",{'product':product})
     
class ProductDetailsView(View):
    def get(self,request,pk):
        totalitem=0
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/productdetail.html",{'product':product})     
    
    
def mobile(request):
 return render(request, 'app/mobile.html')   




class CustomerRegistrationView(View):
    def get(self,request):
      form = CustomerRegistrationForm() 
      totalitem= 0
      wishitem=0
      if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
      return render(request,'app/customerregistration.html',locals())
  
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals()) 
    
    
@login_required        
def add_to_cart(request):
    user = request.user
    produt_id = request.GET.get('prod_id' )  
    product = Product.objects.get(id=produt_id)  
    Cart(user=user,product=product).save()  
    return redirect("/cart")    


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40 
   
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem= 0
        wishitem=0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request): 
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")    
        return render(request,'app/profile.html',locals())

@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user) 
    totalitem= 0
    wishitem=0
    if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/address.html',locals()) 



@method_decorator(login_required,name='dispatch')
class updateAdress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem= 0
        wishitem=0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)  
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfuly")
        else:
            messages.warning(request,"Invalid Input Data")    
        return redirect("address")




def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40    
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data)
    
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40    
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data)    
    
    
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40    
        # print(prod_id)
        data={
            
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data)    
    
 

# @login_required    
# def search(request):
#     query= request.GET['search']   
#     totalitem=0
#     wishitem=0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem= len(Wishlist.objects.filter(user=request.user))
#     product= Product.objects.filter(Q(title__icontains=query))  
#     return render(request,"app/search.html",locals())

class checkout(View):
    def get(self,request):
        totalitem= 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40 
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status,
                
            )
            payment.save()
        return render(request,'app/checkout.html',locals())
    
    

def payment_done(request):
    order_id=request.GET['order_id']
    payment_id=request.GET['payment_id']
    cust_id=request.GET['cust_id']
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

def orders(request):
    totalitem= 0
    wishitem=0
    if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())    

@login_required    
def search(request):
    query= request.GET['search']   
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product= Product.objects.filter(Q(title__icontains=query))  
    return render(request,"app/search.html",locals())
