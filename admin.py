from django.contrib import admin
#from .models import Tracking,userbirthday
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Author)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields =("body",)
    list_display = ["id", "title","images"]
    list_editable=["title"]
admin.site.register(Post,PostAdmin)



admin.site.register(Tracking)
admin.site.register(userbirthday)
admin.site.register(Consultation)




class ProductAdmin_Class(SummernoteModelAdmin):
    summernote_fields =("detail",)
    list_display = ["id","name","available"] #we will show what? in admin page
    list_editable = ["name"]
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id","products"]
    
admin.site.register(Order,OrderAdmin)
    
class TrackingOrderIDAdmin(admin.ModelAdmin):
    list_display = ["id","tracking_order"]
    
admin.site.register(TrackingOrderID,TrackingOrderIDAdmin)    

admin.site.register(Product_model,ProductAdmin_Class)

admin.site.register(Category_model)

admin.site.register(Profile_model)

admin.site.register(Discount_model)



