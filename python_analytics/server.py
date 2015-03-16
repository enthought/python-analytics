from __future__ import absolute_import, unicode_literals

from .event_encoder import TrackedAttribute, EventEncoder


class ServerInfo(object, metaclass=EventEncoder):

    application_name = TrackedAttribute('an', str, required=False)
    response_time = TrackedAttribute('srt', int, required=False)

    def __init__(self, application_name=None, response_time=None):
        if application_name is not None:
            self.application_name = application_name
        if response_time is not None:
            self.response_time = response_time
