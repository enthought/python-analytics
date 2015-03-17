from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


@add_metaclass(EventEncoder)
class ServerInfo(object):

    application_name = TrackedAttribute('an', text_type)
    response_time = TrackedAttribute('srt', int)
