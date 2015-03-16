from __future__ import absolute_import, unicode_literals
from weakref import WeakKeyDictionary


NoValue = object()


class TrackedAttribute(object):

    def __init__(self, target_name, type_, required=True):
        self._name = None
        self._target_name = target_name
        self._type = type_
        self._required = required
        self._data = WeakKeyDictionary()

    def set_attribute_name(self, name):
        self._name = name

    def __get__(self, instance, owner):
        value = self._data.get(instance, NoValue)
        if self._required and value is NoValue:
            raise ValueError(
                'Missing required attribute {!r}'.format(self._name))
        if value is NoValue:
            return None
        return (self._target_name, value)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError('Expected value {!r} to be of type {!r}'.format(
                value, self._type))
        self._data[instance] = value


class Encoder(object):
    def to_dict(self):
        encoded = {}
        for attribute_name in self._tracked_attributes:
            item = getattr(self, attribute_name)
            if item is None:
                continue
            key, value = item
            encoded[key] = value
        return encoded


class EventEncoder(type):

    def __new__(cls, class_name, bases, class_dict):
        bases = (Encoder,) + bases
        tracked_attributes = []
        for key, value in list(class_dict.items()):
            if isinstance(value, TrackedAttribute):
                value.set_attribute_name(key)
                tracked_attributes.append(key)
        class_dict['_tracked_attributes'] = tuple(tracked_attributes)
        return type.__new__(cls, class_name, bases, class_dict)
