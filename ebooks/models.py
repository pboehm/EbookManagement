from django.db import models

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
    group = models.ForeignKey('Group')
    serial = models.IntegerField()

    def __unicode__(self):
        return self.name

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
        try:
            group = Group.objects.get(id=ebook.group.id)
            category = Category.objects.get(id=group.category.id)
            return ("%s/%s/%s" %
                (category.dirname, group.dirname, ebook.filename))
        except Exception, e:
            return ""
