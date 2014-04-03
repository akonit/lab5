from django.contrib import admin
from products.models import Product, Category
from products.forms import ProductForm

class ProductAdmin(admin.ModelAdmin):

    form = ProductForm

    fields = ['name', 'description', 'mark', 'voters', 'categories']
    search_fields = ['description']

    def __init__(self, model, admin_site):
        super(ProductAdmin,self).__init__(model, admin_site)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)