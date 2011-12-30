# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from EbookManagement.ebooks.models import Directory, Ebook
from EbookManagement.settings import *
import os
import time
import re
import sys
import subprocess

class Command(BaseCommand):
    """
        Management-Command welches den Index der Ebooks aktualisiert
    """
    help = 'Updates the Index of Ebooks'

    def handle(self, *args, **options):
        serial_nr = int(time.time())
        os.chdir(EBOOK_PATH)

        ###
        # Alle Top-Level Directories indexieren
        for d in os.listdir(u"."):

            if not os.path.isdir(d) or d.startswith("."):
                continue

            try:
                directory = Directory.objects.get(dirname=d, parent=None)
            except Exception:
                directory = Directory(
                        name=d.replace('_', ' '),
                        dirname=d,
                    )
            directory.serial = serial_nr
            directory.save()

            print "== %s" % directory

            self.update_directory(directory, serial_nr)

        ####
        # Nicht existierende Verzeichnisse Ebooks werden entfernt
        print "Suche nach Ebooks die nicht mehr existieren"
        ser = serial_nr
        for ebook in Ebook.objects.exclude(serial=ser):
            if ebook.hasThumbnail:
                thumbnail = os.path.join(
                                EBOOK_THUMBNAIL_PATH,
                                ebook.hashvalue + '.png'
                            )
                os.unlink(thumbnail)
            print ebook.filename
            ebook.delete()

        for directory in Directory.objects.exclude(serial=ser):
            print directory.dirname
            directory.delete()


    def update_directory(self, directory, serial):
        """
            Dursucht ein Verzeichnis rekursiv und fügt neue
            Ebooks hinzu und aktualisiert die Serial
            von existierenden Verzeichnissen und Ebooks
        """
        for entry in os.listdir(directory.get_relative_path()):

            entry_path = os.path.join(directory.get_relative_path(), entry)
            if os.path.isdir(entry_path):
                ###
                # Ein Verzeichnis, welches indiziert werden muss
                try:
                    subdirectory = Directory.objects.get(dirname=entry, parent=directory)
                except Exception:
                    subdirectory = Directory(
                            name=entry.replace('_', ' '),
                            dirname=entry,
                            parent=directory,
                        )
                subdirectory.serial = serial
                subdirectory.save()

                print ">> %s" % subdirectory

                self.update_directory(subdirectory, serial)

            else:
                ###
                # Es ist ein potentielles Ebook
                print "---> %s" % entry_path
                current_directory = directory

                # Dateiendung extrahieren
                entry_file_ending = ""
                matched_ending = re.match(".*\.(.*)$", entry)

                if matched_ending:
                    entry_file_ending = matched_ending.groups(0)[0]

                try:
                    ebook = Ebook.objects.get(
                                    filename=entry,
                                    directory=current_directory)
                except Exception:
                    ###
                    # Neues Ebook wird verarbeitet
                    filesize = os.path.getsize(entry_path)
                    md5hash = subprocess.Popen(
                                ["md5sum", entry_path],
                                stdout=subprocess.PIPE).communicate()[0].split(' ')[0].strip()

                    print md5hash
                    fileicon = 'file'

                    if entry_file_ending in EXISTING_FILE_ICONS:
                        fileicon = entry_file_ending

                    ebook = Ebook(
                                name=entry,
                                filename=entry,
                                icon=fileicon,
                                directory=current_directory,
                                size=filesize,
                                hasThumbnail=False,
                                hashvalue=md5hash,
                            )

                ###
                # Thumbnail erstellen
                if not ebook.hasThumbnail:
                    entry_thumbnail = os.path.join(
                                        EBOOK_THUMBNAIL_PATH,
                                        ebook.hashvalue + '.png'
                                      )

                    cmd = u'%s "%s" "%s" "%s"' % (
                            os.path.join(PROJECT_ROOT, 'utils', 'create_thumbnail.sh'),
                            os.path.join(EBOOK_PATH, ebook.get_relative_path()),
                            entry_thumbnail,
                            entry_file_ending,
                        )
                    ret = subprocess.call(cmd, shell=True)

                    if ret == 0 and os.path.exists(entry_thumbnail):
                        ebook.hasThumbnail = True

                ebook.serial = serial
                ebook.save()

