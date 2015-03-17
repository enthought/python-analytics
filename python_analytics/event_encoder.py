from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
from weakref import WeakKeyDictionary


NoValue = object()


class _TrackedAttribute(metaclass=ABCMeta):
    def __init__(self, required):
        self._name = None
        self._required = required

    def __get__(self, instance, owner):
        value = self._get_value(instance, owner)
        return self._format(value)

    def __set__(self, instance, value):
        self._check_type(value)
        self._data[instance] = self._coerce(value)

    def set_attribute_name(self, name):
        self._name = name

    def _get_value(self, instance, owner):
        value = self._data.get(instance, NoValue)
        if self._required and value is NoValue:
            raise ValueError(
                'Missing required attribute {!r}'.format(self._name))
        return value

    @abstractmethod
    def _format(self, value):
        pass

    @abstractmethod
    def _coerce(self, value):
        pass


class TrackedAttribute(_TrackedAttribute):

    def __init__(self, target_name, type_=None, required=False):
        super(TrackedAttribute, self).__init__(required)
        self._target_name = target_name
        self._type = type_
        self._data = WeakKeyDictionary()

    def _format(self, value):
        if value is NoValue:
            return None
        return [(self._target_name, value)]

    def _coerce(self, value):
        return value

    def _check_type(self, value):
        if self._type is not None and not isinstance(value, self._type):
            raise TypeError('Expected value {!r} to be of type {!r}'.format(
                value, self._type))


class Encoder(object):
    def to_dict(self):
        encoded = {}
        for attribute_name in self._tracked_attributes:
            item = getattr(self, attribute_name)
            if item is None:
                continue
            encoded.update(item)
        return encoded


class EventEncoder(type):

    def __new__(cls, class_name, bases, class_dict):
        bases = (Encoder,) + bases
        tracked_attributes = []
        for key, value in list(class_dict.items()):
            if isinstance(value, _TrackedAttribute):
                value.set_attribute_name(key)
                tracked_attributes.append(key)
        class_dict['_tracked_attributes'] = tuple(tracked_attributes)
        return type.__new__(cls, class_name, bases, class_dict)
