from django.contrib import admin
from .models import (
    Customer ,
    Product,
    Cart,
    OrderPlaced,
    Payment
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']    
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']   
    
    
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']   
    
    
   