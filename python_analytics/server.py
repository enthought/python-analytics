from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


@add_metaclass(EventEncoder)
class ServerInfo(object):

    application_name = TrackedAttribute('an', text_type)
    response_time = TrackedAttribute('srt', int)

    def __init__(self, application_name=None, response_time=None):
        if application_name is not None:
            self.application_name = application_name
        if response_time is not None:
            self.response_time = response_time
