from typing import Any
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
 #name of class

# Create your models here.
class Tracking(models.Model):  # การสืบทอดความสามาด interic  after that make migration
    name = models.CharField(max_length=100)  #compulsory
    tel = models.CharField(max_length=15)
    Tracking = models.CharField(max_length=100,null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    
    #want to show value of what
    def __str__(self):
        return '{}-{} ({})'.format(self.name, self.tel,self.Tracking)  #do not migrate
    
class userbirthday(models.Model):
    name = models.CharField(max_length=100)
    nationnality = models.CharField(max_length=100)
    birthday = models.DateField(max_length=100)
    
    def __str__(self):
        return '{}-{}-({})'.format(self.name, self.nationnality,self.birthday)
    
#model will use in admin/database
class Consultation(models.Model):
    name = models.CharField(max_length=100,verbose_name='contacter name')
    #verbosename is: name of explanation for backend know
    email = models.CharField(max_length=100,null=True,blank=True,verbose_name='email')
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name='topic')
    detail = models.TextField(null=True,blank=True,verbose_name='detail')
    detail_answer = models.TextField(null=True,blank=True, verbose_name='detailed answer')
def __str__(self):
    return '{}-({})'.format(self.name, self.title)



class Author(models.Model):
    author_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="author-image",null=True,blank=True, default="default.png")
    def __str__(self):
        return self.author_name

class Post(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description=models.TextField(max_length=280,null=True,blank=True)
    body=models.TextField(null=True,blank=True)
    images = models.ImageField(upload_to="post-image",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    data_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,max_length=180,null=True,blank=True)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    
    
class Category_model(models.Model):
    category_name = models.CharField(max_length=255,default="general")
    category_detail = models.TextField(null=True, blank=True)
        
    def __str__(self):
        return self.category_name
class Product_model(models.Model):
    category = models.ForeignKey(Category_model, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    
    normal_price = models.IntegerField(null=True, blank=True) 
    price1 = models.IntegerField(null=True, blank=True) 
    price2 = models.IntegerField(null=True, blank=True)
    shipping_cost =models.IntegerField(default=40,null=True, blank=True)
    
    
    images = models.ImageField(upload_to="products",null=True, blank=True)
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True) #can see or not after upload
    unit = models.CharField(max_length=255,default="-")
    image_url = models.CharField(max_length=255,null=True, blank=True) #its not picture
    created_date = models.DateTimeField(auto_now_add=True) #when create date
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,max_length=180,null=True, blank=True) 
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    products = models.ForeignKey(Product_model,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    lastname_name = models.CharField(max_length=100)
    tel= models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    address = models.TextField()
    count = models.IntegerField(default=1)
    buyer_price = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)
    slip = models.ImageField(upload_to="product-slip/")
    tracking_number = models.CharField(max_length=100,null=True, blank=True)
    not_complete = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name
    
class TrackingOrderID(models.Model):
    tracking_order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_id")
    order_id=models.CharField(max_length=10)
    
    def __str__(self):
        return self.order_id
    
class Profile_model(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #CASCADE:if user is deleted ,profile will be deleted also
    photo = models.ImageField(upload_to='profile_photo',null=True, blank=True)
    usertype = models.CharField(max_length=100,default='member')
    interested_in = models.CharField(max_length=100,null=True,blank=True)
    facebook = models.CharField(max_length=100,default='No Facebook account')
    address =models.TextField(null=True,blank=True)
    tel = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.user.username
    
class Discount_model(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    percent = models.IntegerField(default=10,null=True,blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.percent}% discount"
    
    
    
    
    
    
    
        
 
        