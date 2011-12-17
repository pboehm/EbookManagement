from django.core.management.base import BaseCommand, CommandError
from EbookManagement.ebooks.models import *
from EbookManagement.settings import * 
import os
import time
import subprocess

class Command(BaseCommand):
    """
        Management-Command welches den Index der Ebooks aktualisiert
    """
    help = 'Updates the Index of Ebooks'

    def handle(self, *args, **options):
        serial= int(time.time())  
        os.chdir(EBOOK_PATH)

        """
        iterate over all Groups
        """
        for cat in os.listdir(u"."):

            if not os.path.isdir(cat) or cat.startswith("."):
                continue
        
            print cat
            try:
                existing_category = Category.objects.get(dirname=cat)
            except Exception, e:
                existing_category = Category(
                                        name=cat.replace("_", " "),
                                        dirname=cat)

            existing_category.serial = serial
            existing_category.save()

            """
            iterate over all Groups
            """
            for group in os.listdir(cat):

                if not os.path.isdir(os.path.join(cat,group)) or group.startswith("."):
                    continue
            
                print "--> %s" % group
                try:
                    existing_group = Group.objects.get(
                                        dirname=group,
                                        category=existing_category.id)
                except Exception, e:
                    existing_group = Group(
                                        name=group.replace("_", " "),
                                        dirname=group,
                                        category=existing_category)
    
                existing_group.serial = serial
                existing_group.save()

                """
                iterate over all Ebooks
                """
                for ebook in os.listdir(os.path.join(cat,group)):
                    
                    ebookfile = unicode( os.path.join(cat,group,ebook))
                    if not os.path.isfile(ebookfile or ebook.startswith(".")):
                        continue
                
                    print "----> %s" % ebook
                    try:
                        existing_ebook = Ebook.objects.get(
                                                    filename=ebook,
                                                    group=existing_group.id)
                    except Exception, e:
                        filesize=os.path.getsize(os.path.join(cat,group,ebook))
                        md5hash = subprocess.Popen(["md5sum", ebookfile], stdout=subprocess.PIPE).communicate()[0].split(' ')[0].strip()
                        print md5hash
                        fileicon='file'
                        ending = ebook[-3:].lower()

                        if ending in EXISTING_FILE_ICONS:
                            fileicon = ending 

                        existing_ebook = Ebook(
                                            name=ebook,
                                            filename=ebook,
                                            icon=fileicon,
                                            group=existing_group,
                                            size=filesize,
                                            hasThumbnail=False,
                                            hashvalue=md5hash)
                    
                    """
                    Thumbnail erstellen
                    """
                    if not existing_ebook.hasThumbnail:
                        cmd = u'%s "%s" "%s" "%s"' % (
                                 os.path.join(PROJECT_ROOT, 'utils', 'create_thumbnail.sh'), 
                                 os.path.join(EBOOK_PATH, ebookfile),
                                 os.path.join(EBOOK_THUMBNAIL_PATH, existing_ebook.hashvalue + '.png'),
                                 (ebookfile[-3:].lower())
                               )
                        ret = subprocess.call(cmd, shell=True)
                        if ret == 0:
                            existing_ebook.hasThumbnail = True

                    existing_ebook.serial = serial
                    existing_ebook.save()
        
        """
        Delete Categories, Groups, Ebooks which are not updated
        """

        print "Suche nach Ebooks die nicht mehr existieren"
        ser=serial
        for ebook in Ebook.objects.exclude(serial=ser):
            if ebook.hasThumbnail:
                thumbnail = os.path.join(EBOOK_THUMBNAIL_PATH, ebook.hashvalue + '.png')
                os.unlink(thumbnail)
            print ebook.filename
            ebook.delete()
        
        for group in Group.objects.exclude(serial=ser):
            print group.dirname
            group.delete()
        
        for category in Category.objects.exclude(serial=ser):
            print category.dirname
            category.delete()




