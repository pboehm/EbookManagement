# -*- coding: utf-8 -*-
import pyinotify


class EbookChangeProcessor(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        print "IN CREATE: %s" % event.pathname

    def process_IN_DELETE(self, event):
        print "IN DELETE: %s" % event.pathname
