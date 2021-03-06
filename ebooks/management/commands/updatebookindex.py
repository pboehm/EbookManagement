# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from EbookManagement.ebooks.models import Directory, Ebook
from EbookManagement.settings import *
from optparse import make_option
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
    option_list = BaseCommand.option_list + (
        make_option('--quiet',
            action='store_true',
            dest='quiet',
            default=False,
            help='Keine Ausgaben'),
        )

    def handle(self, *args, **options):
        self.quiet = options.get("quiet")
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

            if not self.quiet:
                print "== %s" % directory

            self.update_directory(directory, serial_nr)

        ####
        # Nicht existierende Verzeichnisse Ebooks werden entfernt
        if not self.quiet:
            print "Suche nach Ebooks die nicht mehr existieren"

        ser = serial_nr
        for ebook in Ebook.objects.exclude(serial=ser):
            if not self.quiet:
                print ebook.filename
            ebook.delete()

        for directory in Directory.objects.exclude(serial=ser):
            if not self.quiet:
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

                if not self.quiet:
                    print ">> %s" % subdirectory

                self.update_directory(subdirectory, serial)

            else:
                ###
                # Es ist ein potentielles Ebook
                if not self.quiet:
                    print "---> %s" % entry_path
                current_directory = directory

                # Index-Dateien ausschließen
                isIndexfile = re.match("^\.fileinfo\..*$", entry)
                if isIndexfile:
                    continue

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

                    #print md5hash
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

                ebook.serial = serial
                ebook.save()

