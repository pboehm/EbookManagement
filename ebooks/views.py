# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import *
from EbookManagement.settings import *
from EbookManagement.ebooks.forms import *
import os
import re
import pprint
import shutil

@login_required
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

@login_required
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
            
            action_form = EbookActionSelectForm()

            return render_to_response('list_ebooks.html',
                    {'group': group.name, 'ebooks': ebooks, 'action': action_form})
        except Exception, e:
            return HttpResponseNotFound
        
    elif type == "ebook":
        pass
        
    else:
        return HttpResponseNotFound

@login_required
def manage_ebooks(request):
    """
        Ebooks verwalten
    """
    if request.POST is None:
        return HttpResponseRedirect("/")

    ###
    # Ebook-IDs extrahieren
    ebook_ids = []
    action=""
    for (key, value) in request.POST.iteritems():
        if (len(value) != 0) and key.endswith('selected'): 
            try:
                e_id = key.split('-')[0]
                Ebook.objects.get(id=e_id)
                ebook_ids.append(e_id)
            except Exception, e:
                pass
        elif key == 'action':
            action = value

    if len(ebook_ids) == 0 or action == '':
        return HttpResponseRedirect("/")

    ###
    # Action entsprechend auswerten
    if action == 'info':
        print "Info"
    elif action == 'move':
        forms = []
        for i in ebook_ids:
            try:
                ebook = Ebook.objects.get(id=i)
                form = EbookMovementForm(instance=ebook, prefix=i)
                forms.append(form)
            except Exception, e:
                pass
        
        return render_to_response('move_ebooks.html', {'forms': forms})        

    elif action == 'delete':
        print "Delete"
    elif action == 'push2kindle':
        print "Push2Kindle"

    return HttpResponseRedirect("/")

@login_required
def submit_ebook_move(request):
    """
        Ebooks letztendlich verschieben
    """
    
    # verwendete IDs extrahieren
    ids = []
    for (key,value) in request.POST.iteritems():
        match = re.search('(\d+)-name$', key)
        if match and (match.group(1) not in ids ):
            ids.append(match.group(1))

    ###
    # Alle Forms aus POST extrahieren
    for i in ids:
        form = EbookMovementForm(data=request.POST, prefix=i)
        if form.is_valid():
            try:
                ebook = Ebook.objects.get(id=i)
                currentGroup = ebook.group
                newGroup = form.cleaned_data['group']

                if currentGroup != newGroup:
                    ###
                    # Dateien verschieben und Model anpassen
                    currPath = newPath = ""
                    currPath = os.path.join(MEDIA_ROOT, ebook.get_relative_path())
                    ebook.group = newGroup
                    newPath = os.path.join(MEDIA_ROOT, ebook.get_relative_path())
                    
                    shutil.move(currPath, newPath)
                    if os.path.exists(newPath): 
                        ebook.save()
            except Exception, e:
                print e

    return HttpResponseRedirect("/")

