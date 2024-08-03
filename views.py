import string
import random

from django.shortcuts import render, get_object_or_404,redirect #to check error o not

from django.http import HttpResponse
# from .models import Tracking
from .models import *
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
# Create your views here.
#M T V (Models template Views)
# def index(request):
#     return redirect('home')
from django.core.files.storage import FileSystemStorage

def Home(request):
    return render(request,'myapp/home.html')
def aboutus(request):
    return render(request,'myapp/aboutus.html')
def contact(request):
    return render(request,'myapp/contact.html')
def tracking(request):
    #tracking=['Mrx-TA318237sffa3','Mry-TA3182jksssf3','Mrx-TA3rkdfs82373','aiy-632747384'] 
    tracking = Tracking.objects.all()  #obkect.filter(name='aiy')
    #name of function =! name of model is important  if not it will error!!!
    context = {'tracking': tracking}
    return render(request,'myapp/tracking.html',context)

def Consult(request):
    if request.method == 'POST':
       data=request.POST.copy()
       #print('DATA:',data)
       name = data.get('name')
       email = data.get('email')
       title=data.get('title')
       detail=data.get('detail')
       print(name,email,title,detail)
       
       new = Consultation()
       new.name=name
       new.email=email
       new.title=title
       new.detail=detail
       new.save()
       
    return render(request,'myapp/consult.html')

@login_required #normally we do not use cause its advance
def Questions(request):
    questions = Consultation.objects.all()  
    context = {'questions': questions}
    return render(request,'myapp/questions.html',context)


def Answer(request,consult_id):
    record = Consultation.objects.get(id=consult_id) # use with id
    #convey record into html
    
    if request.method == 'POST':
       data=request.POST.copy()
       #print('DATA:',data)
       #Consult_id = data.get('consult_id')
       detail_answer =data.get('detail_answer')
       record.detail_answer= detail_answer
       record.save()
    context={'record':record}  #thing is saved in Consultation(model)
    #in order to send to form (answer.html)
    
    return render(request,'myapp/answer.html',context)




def Sabaidee(request):
    return HttpResponse('<h1 style="color:red">ສະບາຍດີ</h1>')



def Posts(request):
    posts = Post.objects.all().order_by('id').reverse()[:6]
    context = {"posts": posts}

    return render(request,'myapp/blog.html',context)


#create detailed blogs function 
#slug to hide id
def PostDetail(request, slug):
    posts = Post.objects.all().order_by('id').reverse()[:6]
    #ดึงข้อมูลทังหมดมา  old-->new
    
    try:
        single_post = get_object_or_404(Post,slug=slug)#Post model
        print("detailed acticles", single_post)
    except Post.DoesNotExist: #if not see data
        return render(request,'myapp/home.html')
    
    context = {"single_post":single_post,"posts":posts} #a page
    #return page that we want
    return render(request,'myapp/blog.detail.html',context)




def Register(request):
    
    context = {} 
    
    if request.method == 'POST':
       data = request.POST.copy()
       name = data.get('name')
       email = data.get('email')
       password = data.get('password')
       
       check =User.objects.filter(username=email)
       print('CHECK:',check)
       print('COUNT:',len(check))
       
       if len(check) == 0:
         newuser= User() #User() is model in django already
         newuser.username=email
         newuser.first_name=name
         newuser.set_password(password)#is method to set password
         newuser.save()
         
        #  profile = Profile_model()
        #  profile.user= newuser
        #  profile.save()
         
         
         context['success']='success'
       else:
           context['usertaken']='usertaken'
       
    return render(request,'myapp/register.html',context)








def Login(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        email = data.get('email')
        password = data.get('password')

        # Check if the user exists
        user_exists = User.objects.filter(username=email).exists()

        if not user_exists:
            context['noUser'] = 'noUser'
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                print('login completed!')
                return redirect('home')
            else:
                context['wrongpassword'] = 'wrongpassword'

    return render(request, 'myapp/login.html', context)


    


@login_required
def AllProduct_def(request):
    all_product = Product_model.objects.filter(available=True)
    
    # # Fetch the user's profile
    # user_profile = Profile_model.objects.get(user=request.user)
    # user_discount = Discount_model.objects.get(user=request.user)
    # print("ALL Product", all_product)
    
    # Fetch the user's profile
    user_profile = get_object_or_404(Profile_model, user=request.user)
    
    # Fetch the user's discount if it exists
    try:
        user_discount = Discount_model.objects.get(user=request.user)
    except Discount_model.DoesNotExist:
        user_discount = None  # Handle case where user has no discount
    
    # Print all products for debugging
    print("ALL Product", all_product)
    
    # Include the user and profile in the context
    context = {
        "all_product": all_product,
        "user": request.user,
        "user_profile": user_profile,
        "user_discount": user_discount,
    }
    
    return render(request, "myapp/all-product.html", context)





# def DiscountPage_def(request):
    
#     if request.user.discount.active == True:
#         return redirect('all-products-link')
    
    
    
#     context = {} 
    
#     if request.method == 'POST':
#        data = request.POST.copy()
#        name = data.get('name')
#        check = data.get('discount')
#        print('CHECK:',check)
#        if check == 'check-true':
#         #    request.user.discount.active = True
#           user = User.objects.get(username=request.user.username)
#           discount = Discount_model.objects.get(user=user)
#           discount.active = True
#           discount.save()
#           return redirect('all-products-link')
       
#     return render(request,'myapp/discount.html',context)

@login_required
def DiscountPage_def(request):
    try:
        discount = Discount_model.objects.get(user=request.user)
    except Discount_model.DoesNotExist:
        discount = None

    if discount and discount.active:
        return redirect('all-products-link')

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        check = data.get('discount')

        if check == 'check-true':
            discount, created = Discount_model.objects.get_or_create(user=request.user)
            discount.active = True
            discount.save()
            return redirect('all-products-link')

    return render(request, 'myapp/discount.html', context)



# def ProductDetail_def(request,slug):
#     product =Product_model.objects.get(slug=slug)
    
#     context = {"product": product}
#     if product.price1 >0:
#         price_1 = (product.price1 * 100) / product.normal_price
#         context["price_1"]=100-int(price_1)
#         context["product_price"]=product.price1
    
#     if product.price2>0:
#         price_2 = (product.price2 * 100) / product.normal_price
        
#         context["price_2"]=100-int(price_2)
        
#     if request.method == "POST":
#         data = request.POST.copy()
#         new_order =Order()
#         new_order.products = product
#         new_order.first_name = data.get("first_name")
#         new_order.lastname_name = data.get("last_name")
#         new_order.tel = data.get("tel")
#         new_order.email = data.get("email")
#         new_order.address = data.get("address")
#         new_order.count = data.get("count")
#         new_order.buyer_price = data.get("buyer_price")
#         new_order.shipping_cost = data.get("shipping_cost")
        
#         try:
#             file_image = request.FILES['upload_slip']
#             file_image_name = request.FILES["upload_slip"].name.replace(" ", "")
#             file_system_storage = FileSystemStorage()
#             file_name = file_system_storage.save("product-slip/"+file_image_name,file_image)
#             upload_file_url = file_system_storage.url(file_name)
#             new_order.slip = upload_file_url[6:]
            
#         except:
#             new_order.slip ="/default.png"
            
#             new_order.save()
            
#     return render(request, "myapp/product-detail.html", context)

def RandomOrderID():
    random_order_id = ""
    random_order_id += random.choice(string.ascii_uppercase) 
    random_order_id += random.choice(string.ascii_uppercase)
    
    for i in range(8):
        random_order_id += random.choice("0123456789")
    return random_order_id


def ProductDetail_def(request, slug):
    RandomOrderID()
    
    product = Product_model.objects.get(slug=slug)
    context = {"product": product, "product_price": product.normal_price}

    if product.price1 > 0:
        price_1 = (product.price1 * 100) / product.normal_price

        context["price_1"] = 100 - int(price_1)
        context["product_price"] = product.price1
    if product.price2 > 0:
        price_2 = (product.price2 * 100) / product.normal_price

        context["price_2"] = 100 - int(price_2)

    if request.method == "POST":
        data = request.POST.copy()
        new_order = Order()
        # new_order.user = product
        new_order.products = product
        new_order.first_name = data.get("first_name")
        new_order.lastname_name = data.get("last_name")
        new_order.tel = data.get("tel")
        new_order.email = data.get("email")
        new_order.address = data.get("address")
        new_order.count = data.get("count")
        new_order.buyer_price = data.get("buyer_price")
        new_order.shipping_cost = data.get("shipping_cost")
        try:
            file_image = request.FILES["upload_slip"]
            file_image_name = request.FILES["upload_slip"].name.replace(" ", "")
            file_system_storage = FileSystemStorage()
            file_name = file_system_storage.save(
                "products-slip/" + file_image_name, file_image
            )
            upload_file_url = file_system_storage.url(file_name)
            new_order.slip = upload_file_url[6:]
        except:
            new_order.slip = "/default.png"


        new_order.save()
        #add function for random id
        try:
            tracking_id = TrackingOrderID.objects.all()
            while True:
                order_ID = RandomOrderID()
                for trackingid in tracking_id:
                    if order_ID == trackingid.order_id:
                        continue
                break
        except:
            order_ID = RandomOrderID()
        new_tracking_id = TrackingOrderID()
        new_tracking_id.tracking_order=new_order
        new_tracking_id.order_id=order_ID
        new_tracking_id.save()
        
        return redirect("tracking-order-id-page",order_ID)
        

    return render(request, "myapp/product-detail.html", context)
def TrackingOrderID_def(request,trackingid):
    tracking_id = TrackingOrderID.objects.get(order_id=trackingid).tracking_order
    buyer_price = tracking_id.buyer_price
    
    if buyer_price == int(buyer_price):
        buyer_price = int(buyer_price)
        
    shipping_cost = tracking_id.shipping_cost
    if shipping_cost == int(shipping_cost):
        shipping_cost = int(shipping_cost)
    all_price = tracking_id.buyer_price + tracking_id.shipping_cost
    context = {
       "tracking_id": tracking_id,
       "buyer_price": buyer_price,
       "order_id": trackingid,
       "shipping_cost": shipping_cost,
       "all_price": all_price
    }
    return render(request, "myapp/tracking-order.html", context)