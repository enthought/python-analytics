from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


@add_metaclass(EventEncoder)
class Event(object):

    hit = TrackedAttribute('t', text_type, required=True)
    category = TrackedAttribute('ec', text_type, required=True)
    action = TrackedAttribute('ea', text_type, required=True)
    label = TrackedAttribute('el', text_type)
    value = TrackedAttribute('ev', int)

    def __init__(self, **kwargs):
        self.hit = 'event'
        for name, value in kwargs.items():
            setattr(self, name, value)
