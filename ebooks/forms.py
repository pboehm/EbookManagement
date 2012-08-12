# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form
from ebooks.models import Ebook
from django import forms
import settings


class EbookForm(ModelForm):
    class Meta:
        model = Ebook


class EbookUploadForm(Form):
    file = forms.FileField()


class EbookManagementForm(Form):
    selected = forms.BooleanField()


class EbookActionSelectForm(Form):
    action = forms.ChoiceField(choices=settings.CHOICES_FOR_EBOOKS)


class EbookMovementForm(ModelForm):
    class Meta:
        model = Ebook
        fields = ('name', 'directory')
