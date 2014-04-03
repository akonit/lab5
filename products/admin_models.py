from django.db import models
from django import forms
from djangotoolbox.fields import EmbeddedModelField, ListField
import ast

#ListField implementations and visualisation
class ListFieldWidget(forms.SelectMultiple):
    pass

class CategoryListFormField(forms.MultipleChoiceField):
    widget = ListFieldWidget

    def clean(self, value):
        return value

class OpinionField(ListField):
    def formfield(self, **kwargs):
        return None
    
    def __init__(self, *args, **kwargs):
        super(OpinionField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class ProductField(ListField):
    def formfield(self, **kwargs):
        return None

    def __init__(self, *args, **kwargs):
        super(ProductField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class CategoryField(ListField):
    def formfield(self, **kwargs):
        return CategoryListFormField(**kwargs)

    def __init__(self, *args, **kwargs):
        super(CategoryField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)