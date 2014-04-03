from django.db import models
from django import forms
from djangotoolbox.fields import EmbeddedModelField, ListField
from products.admin_models import ProductField, CategoryField, OpinionField

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    mark = models.DecimalField(max_digits=10, decimal_places=5)
    voters = models.IntegerField(default=0)
    opinions = OpinionField(EmbeddedModelField('Opinion'))
    categories = CategoryField()

    def __unicode__(self):
        return self.name

class Opinion(models.Model):
    login = models.CharField(max_length=64)
    text = models.CharField(max_length=512)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text

    @classmethod
    def create(cls):
        opinion = cls()
        return opinion

class Category(models.Model):
    name = models.CharField(max_length=64)
    products = ProductField()

    def __unicode__(self):
        return self.name