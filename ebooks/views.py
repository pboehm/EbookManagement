# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
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
    toplevel_dirs = []
    for directory in Directory.objects.order_by("name").filter(parent=None):
        toplevel_dirs.append(directory)

    return render_to_response(
                'item_list.html',
                {
                    'directories': toplevel_dirs,
                    'dir_count': len(toplevel_dirs),
                    'sitetitle': "Verzeichnisuebersicht",
                },
                context_instance=RequestContext(request)
            )

@login_required
def show_data(request, type, dataid):
    """
        Listet Ebooks und Verzeichnisse auf
    """
    if type == "directory":
        try:
            directory = Directory.objects.get(id=dataid)

            subdirs = directory.get_directories()

            ebooks = []
            for ebook in directory.get_ebooks():
                form = EbookManagementForm(prefix=str(ebook.id))
                info = EbookInformation(ebook, form)
                ebooks.append(info)
            action_form = EbookActionSelectForm()

            return render_to_response(
                        'item_list.html',
                        {
                            'sitetitle': 'Inhalt von "%s"' % directory.name,
                            'directories': subdirs,
                            'dir_count': len(subdirs),
                            'ebooks': ebooks,
                            'ebook_count': len(ebooks),
                            'action': action_form
                        },
                        context_instance=RequestContext(request))
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

        return render_to_response('move_ebooks.html', {'forms': forms},
                context_instance=RequestContext(request))

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
    for (key, value) in request.POST.iteritems():
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

