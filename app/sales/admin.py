from django.contrib import admin
from . models import SaleGroup
from . models import Sale

# Register your models here.

admin.site.register(Sale)
admin.site.register(SaleGroup)

