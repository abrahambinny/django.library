'''
API Admin File to regitster the models in admin
'''

from django.contrib import admin
from .models import Book, Wishlist

# Register your models here.
admin.site.register(Book)
admin.site.register(Wishlist)
