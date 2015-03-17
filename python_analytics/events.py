from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


class _CustomField(object):

    FORMAT = None

    def __init__(self, index, value):
        self._index = index
        self._value = value

    @property
    def key(self):
        return self.FORMAT.format(self._index)

    @property
    def value(self):
        return self._value


class CustomDimension(_CustomField):

    FORMAT = 'cd{:d}'


class CustomMetric(_CustomField):

    FORMAT = 'cm{:d}'


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
