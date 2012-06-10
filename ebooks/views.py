# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from models import *
from EbookManagement.settings import *
from EbookManagement.ebooks.forms import *
import os
import re
import shutil
import json

@login_required
def overview(request):
    """
        Gibt einen Überblick über vorhandene Kategorien und Gruppen
    """
    toplevel_dirs = []
    for directory in Directory.objects.order_by("name").filter(parent=None):
        toplevel_dirs.append(directory)

    recent_ebooks = []
    for ebook in Ebook.objects.order_by("-indexed").all()[:5]:
        recent_ebooks.append(ebook)

    return render_to_response(
                'overview.html',
                {
                    'directories': toplevel_dirs,
                    'recent_ebooks': recent_ebooks,
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
                        'directory_listing.html',
                        {
                            'current_directory': directory,
                            'directories': subdirs,
                            'ebooks': ebooks,
                            'action': action_form
                        },
                        context_instance=RequestContext(request))
        except Exception:
            return HttpResponseNotFound

    elif type == "ebook":
        pass

    else:
        return HttpResponseNotFound


def studip_json_data(request):
    """
        Die Inhalte eines StudIP Verzeichnis als JSON zurückgeben,
        um es in Auditorium einbauen zu können.

        Hier absichtlich ohne Authentifizierungszwang
    """
    studip = get_object_or_404(Directory, dirname="StudIP")

    data_for_json = dict()
    for subdir in studip.get_directories():
        ebooks = []

        for ebook in subdir.get_ebooks():
            ebook_info = {
                'name': ebook.name,
                'size': ebook.size,
                'url': "http://" + request.get_host() +
                    urlencode(MEDIA_URL + ebook.get_relative_path()),
            }
            ebooks.append(ebook_info)

        data_for_json[subdir.dirname] = ebooks

    json_serialized = json.dumps(data_for_json, ensure_ascii=False)

    # use JSONP if the parameter callback is supplied
    if request.GET.has_key('callback'):
        json_serialized = "%s(%s)" % (request.GET['callback'], json_serialized)

    return HttpResponse(json_serialized, mimetype='application/json')


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
            except Exception:
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
            except Exception:
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

@login_required
def search_items(request):
    """Suche nach bestimmten Ebooks"""

    if 'query' in request.GET:
        query = request.GET['query']

        ebooks = []
        for ebook in Ebook.objects.order_by("name").filter(filename__icontains=query):
            form = EbookManagementForm(prefix=str(ebook.id))
            info = EbookInformation(ebook, form)
            ebooks.append(info)
        action_form = EbookActionSelectForm()

        return render_to_response(
                'search_results.html',
                {
                    'search_query': query,
                    'ebooks': ebooks,
                    'action': action_form
                },
                context_instance=RequestContext(request)
            )
    return HttpResponseRedirect("/")

@login_required
def add_ebook(request):
    if request.method == 'POST':
        form = EbookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES['file'].name
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = EbookUploadForm()
    return render_to_response(
                'ebook_upload.html',
                {
                    'upload_form': form,
                },
                context_instance=RequestContext(request)
            )

@login_required
def manage_user_profile(request):
    """docstring for manage_user_profile"""
    return HttpResponseRedirect("/")
