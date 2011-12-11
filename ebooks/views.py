# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect
from forms import *
from models import *
from EbookManagement.settings import *
from EbookManagement.ebooks.forms import EbookManagementForm
import os
import pprint
import re

def overview(request):
    """
        Gibt einen Überblick über vorhandene Kategorien und Gruppen
    """
    categories = []
    for cat in Category.objects.order_by("name").all():
        categorywithgroups = CategoryWithGroups(cat)
    
        for group in Group.objects.order_by("name").filter(category=cat.id):
            categorywithgroups.addGroup(group)

        categories.append(categorywithgroups)
    
    return render_to_response('overview.html', { 'categories': categories})

    
def show_data(request, type, dataid):
    """
        Listet verschiedene Daten auf
    """
    if type == "group":
        try:
            group = Group.objects.get(id=dataid)
            ebooks = []
            for ebook in Ebook.objects.order_by("name").filter(group=group.id):
                form = EbookManagementForm(prefix=str(ebook.id))
                info = EbookInformation(ebook, form)
                ebooks.append(info)
                
            return render_to_response('list_ebooks.html',
                {'group': group.name, 'ebooks': ebooks})
        except Exception, e:
            return HttpResponseNotFound
        
    elif type == "ebook":
        pass
        
    else:
        return HttpResponseNotFound

def manage_ebooks(request):
    """
        Ebooks verwalten
    """
    pp = pprint.PrettyPrinter()

    if request.POST is not None:
        for (key, value) in request.POST.iteritems():
            if (len(value) != 0) and EbookManagementForm.isValidAction(value):
                print value

    return HttpResponseRedirect('/')

"""
def submit_new(request, type):
   
        Neue Daten hinzufügen
   
    if type == "ebook":
        form=EbookForm(request.POST)
        if form.is_valid():
            f=form.cleaned_data["filename"]
            n=form.cleaned_data["name"]
            g=form.cleaned_data["group"]
            s=form.cleaned_data["size"]

            ebook = Ebook(filename=f, name=n, group=g, size=s)
            ebook.save()
            
            return HttpResponseRedirect('/')
        else:
            return render_to_response('add_new.html',
                { 'sitetitle': 'Fehler im Formular', 'form': form, 'type': type})
        
"""
