from mongoengine import *

import datetime


class Trace(Document):

    __required = ['type', 'token']

    #__date_format = '%Y-%m-%d'

    type = StringField(required=True)
    token = StringField(required=True)
    message = StringField()
    stack = ListField()
    context = StringField()

    """ pre-save validation """
    def clean(self):

        # verify required fields
        missing = []
        for field in self.__required:
            if field not in self:
                missing.append(field)
            elif not self[field]:
                missing.append(field)
        if missing:
            raise ValueError("Missing required property: %s" %
                             ", ".join(missing))

        return True

    def get_id(self):
        return str(self.pk)

    def get_date(self):
        return self.added.strftime(self.__date_format)


class Bucket(Document):

    __required = ['name']

    name = StringField(required=True)

    def clean(self):

        # verify required fields
        missing = []
        for field in self.__required:
            if field not in self:
                missing.append(field)
            elif not self[field]:
                missing.append(field)
        if missing:
            raise ValueError("Missing required property: %s" %
                             ", ".join(missing))

    def get_token(self):
        return str(self.pk)
