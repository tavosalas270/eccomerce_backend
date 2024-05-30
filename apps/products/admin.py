from django.contrib import admin
from apps.products.models import *

# Register your models here.
class MeasureUnitAdmin(admin.ModelAdmin): # Asi muestras los campos que quieras en la vista admin
    list_display = ('id', 'description')

class CategoryProductAdmin(admin.ModelAdmin): # Asi muestras los campos que quieras en la vista admin
    list_display = ('id', 'description')

admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Indicator)
admin.site.register(Product)