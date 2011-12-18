# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form
from models import *
from django import forms
from EbookManagement.settings import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category

class GroupForm(ModelForm):
    class Meta:
        model = Group

class EbookForm(ModelForm):
    class Meta:
        model = Ebook

class EbookManagementForm(Form):
    selected = forms.BooleanField()

class EbookActionSelectForm(Form):
    action = forms.ChoiceField(choices=CHOICES_FOR_EBOOKS)

class EbookMovementForm(ModelForm):
    class Meta:
        model = Ebook
        fields = ('name', 'group')
