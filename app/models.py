from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.

STATE_CHOICES = (
     ('Mahim','Mahim'),
    ('Béja','Béja'),
    ('Ben Arous','Ben Arous'),
    ('Bizerte','Bizerte'),
    ('Gabès','Gabès'),
    ('Gafsa','Gafsa'),
    ('Jendouba','Jendouba'),
    ('Kairouan','Kairouan'),
    ('Kasserine','Kasserine'),
    ('Kebili','Kebili'),
    ('Kef','Kef'),
    ('Mahdia','Mahdia'),
    ('Manouba','Manouba'),
    ('Medenine','Medenine'),
    ('Monastir','Monastir'),
    ('Nabeul','Nabeul'),
    ('Sfax','Sfax'),
    ('Sidi Bouzid','Sidi Bouzid'),
    ('Sousse','Sousse'),
    ('Tataouine','Tataouine'),
    ('Tozeur','Tozeur'),
    ('Tunis','Tunis'),
    ('Zaghouan','Zaghouan'),   
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
    
  
    
CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)   

# class Product(models.Model):
#     titre = models.CharField(max_length=100)
#     selling_price = models.FloatField()
#     discounted_price = models.FloatField()
#     description = models.TextField()
#     brand = models.CharField(max_length=100)
#     category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
#     product_image = models.ImageField(upload_to='productimg')
    
#     def __str__(self):
#       return str(self.id)
  
  
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.title  
  
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
  
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)  


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


    
    
    
  
    



    