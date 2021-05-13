from django.contrib import admin

# Register your models here.
from .models import Category,Product,Preferences

#admin.site.register(Category)
#admin.site.register(Product)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Preferences)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price',
                    'available','created','updated']
    list_filter = ['available','created','updated']
    list_editable = ['price','available']
    prepopulated_fields = {'slug': ('name',)}