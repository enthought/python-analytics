from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import Parameter, EventEncoder


@add_metaclass(EventEncoder)
class Event(object):

    hit = Parameter('t', text_type, required=True)
    category = Parameter('ec', text_type, required=True)
    action = Parameter('ea', text_type, required=True)
    label = Parameter('el', text_type)
    value = Parameter('ev', int)

    def __init__(self, **kwargs):
        self.hit = 'event'
        for name, value in kwargs.items():
            setattr(self, name, value)
