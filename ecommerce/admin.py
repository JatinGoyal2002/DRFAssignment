from django.contrib import admin
from ecommerce.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Image)
admin.site.register(Collection)
admin.site.register(Category)