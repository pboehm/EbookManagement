from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    dirname = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    serial = models.IntegerField()

    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=40)
    dirname = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey('Category')
    serial = models.IntegerField()

    def __unicode__(self):
        return self.name

class Ebook(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    filename = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    group = models.ForeignKey('Group')
    hashvalue = models.CharField(max_length=100)
    hasThumbnail = models.BooleanField()
    serial = models.IntegerField()

    def __unicode__(self):
        return self.name
    
    def get_relative_path(self):
        return os.path.join(self.group.category.dirname, 
                            self.group.dirname,
                            self.filename) 

"""
    Utility-Klassen
"""
class CategoryWithGroups(object):
    def __init__(self, category):
        self.category = category
        self.groups = []

    def addGroup(self, group):
        self.groups.append(group)

class EbookInformation(object):
    def __init__(self, ebook, form):
        self.ebook = ebook
        self.filepath = self.__generate_path(ebook);
        self.form = form

    def __generate_path(self, ebook):
        return ebook.get_relative_path()

