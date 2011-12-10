from django.forms import ModelForm
from models import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category

class GroupForm(ModelForm):
    class Meta:
        model = Group

class EbookForm(ModelForm):
    class Meta:
        model = Ebook
