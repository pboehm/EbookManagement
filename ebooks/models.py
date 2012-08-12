# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os


class Directory(models.Model):
    name = models.CharField(max_length=100)
    dirname = models.CharField(max_length=100)
    parent = models.ForeignKey('Directory', null=True)
    description = models.CharField(max_length=100, blank=True)
    serial = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_relative_path(self):
        path = ""
        for d in self.get_relative_path_components():
            path = os.path.join(path, d.dirname)
        return path

    def get_relative_path_components(self):
        components = []
        c = self
        while c is not None:
            components.insert(0, c)
            c = c.parent
        return components

    def has_ebooks(self):
        try:
            Ebook.objects.get(directory=self)
        except Exception:
            return False
        return True

    def get_ebooks(self):
        ebooks = []
        try:
            for ebook in Ebook.objects.order_by('name').filter(directory=self):
                ebooks.append(ebook)
        except Exception:
            pass
        return ebooks

    def get_directories(self):
        dirs = []
        try:
            for d in Directory.objects.order_by('name').filter(parent=self):
                dirs.append(d)
        except Exception:
            pass
        return dirs


class Ebook(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    filename = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    directory = models.ForeignKey('Directory')
    hashvalue = models.CharField(max_length=100)
    hasThumbnail = models.BooleanField()
    serial = models.IntegerField()
    indexed = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_relative_path(self):
        return os.path.join(self.directory.get_relative_path(),
                            self.filename)


class UserProfile(models.Model):
    """
        Model, welches zusätzliche Informationen über einen
        Nutzer speichert
    """
    user = models.OneToOneField(User)
    hasKindle = models.BooleanField()
    KindleAddress = models.EmailField()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class EbookInformation(object):
    def __init__(self, ebook, form):
        self.ebook = ebook
        self.filepath = self.__generate_path(ebook)
        self.form = form

    def __generate_path(self, ebook):
        return ebook.get_relative_path()
