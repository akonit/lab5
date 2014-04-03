from django.db import models
from django import forms
from djangotoolbox.fields import EmbeddedModelField, ListField
import ast
from products.models import Product, Category, Opinion
from products.admin_models import CategoryListFormField
from django.forms import ModelForm, Textarea
from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch.dispatcher import receiver

#CRUD page for Product
class ProductForm(forms.ModelForm):
    categories = CategoryListFormField()
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['categories'].widget.choices = [(i.name, i) for i in Category.objects.all()]
        if self.instance.name:
            cf = []
            for category in self.instance.categories:
                c = Category.objects.get(id=category)
                cf.append(str(c.name))
            self.fields['categories'].initial = cf

    def save(self, *args, **kwargs):
        instance = super(ProductForm, self).save(commit=False)

        #replace categories names with ids
        cf = []
        for category in instance.categories:
            c = Category.objects.get(name=category)
            cf.append(c.id)
        instance.categories = cf

        #from tulpe to listField
        flatten_opinions = []
        for opinion in instance.opinions:
            old_opinion = Opinion.create()
            old_opinion.login = opinion[1]["login"]
            old_opinion.text = opinion[1]["text"]
            old_opinion.pub_date = opinion[1]["pub_date"]
            flatten_opinions.append(old_opinion)
        instance.opinions = flatten_opinions

        instance.save()

        #remove product from all categories
        categories = Category.objects.all()
        for category in categories:
            products = []
            for product in category.products:
                if product == instance.id:
                    continue
                if product != instance.id:
                    products.append(product)
            category.products = products
            category.save()

        #add product to involved categories
        categories = Category.objects.filter(id__in = instance.categories)
        for category in categories:
            category.products.append(instance.id)
            category.save()

        #just suppress this method
        def save_m2m():  
            number=1 

        self.save_m2m = save_m2m
        self.save_m2m()
     
        return instance

    class Meta:
        model = Product


@receiver(pre_delete, sender=Product)
def _product_delete(sender, instance, **kwargs):
    categories = Category.objects.filter(id__in = instance.categories)
    for category in categories:
        products = []
        for product in category.products:
            if product == instance.id:
                continue
            if product != instance.id:
                products.append(product)
        category.products = products
        category.save()

@receiver(m2m_changed, sender=Product)
def _stub_product_m2m(sender, instance, **kwargs):
    stub = None

@receiver(pre_delete, sender=Category)
def _category_delete(sender, instance, **kwargs):
    products = Product.objects.filter(id__in = instance.products)
    for product in products:
        categories = []
        for category in product.categories:
            if category == instance.id:
                continue
            if category != instance.id:
                categories.append(category)
        product.categories = categories
        product.save()

@receiver(m2m_changed, sender=Category)
def _stub_category_m2m(sender, instance, **kwargs):
    stub = None

class OpinionForm(ModelForm):
   class Meta:
        model = Opinion
        exclude = ["post"]
        fields = ['login', 'text']
        labels = {
            'text': ('Opinion'),
        }
        widgets = {
            'text': Textarea(attrs={'cols': 30, 'rows': 10}),
        }