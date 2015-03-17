from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
from weakref import WeakKeyDictionary

from six import add_metaclass, text_type


NoValue = object()


@add_metaclass(ABCMeta)
class _TrackedAttribute(object):
    def __init__(self, type_, required):
        self._name = None
        self._required = required
        self._type = type_
        self._data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        value = self._get_value(instance, owner)
        return self._format(value)

    def __set__(self, instance, value):
        if self._type is not None and not isinstance(value, self._type):
            raise TypeError('Expected value {!r} to be of type {!r}'.format(
                value, self._type))
        self._data[instance] = value

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
        """Format the key and value for Google Analytics.

        """


class TrackedAttribute(_TrackedAttribute):

    def __init__(self, target_name, type_=None, required=False):
        super(TrackedAttribute, self).__init__(type_, required)
        self._target_name = target_name

    def _format(self, value):
        if value is NoValue:
            return None
        return (self._target_name, value)


class _CustomAttribute(_TrackedAttribute):

    FORMAT = None
    TYPE = None

    def __init__(self, index, required=False):
        super(_CustomAttribute, self).__init__(self.TYPE, required)
        self._index = index

    def _format(self, value):
        if value is NoValue:
            return None
        return (self.FORMAT.format(self._index), value)


class CustomDimension(_CustomAttribute):

    FORMAT = 'cd{:d}'
    TYPE = text_type


class CustomMetric(_CustomAttribute):

    FORMAT = 'cm{:d}'
    TYPE = int


class Encoder(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if name not in self._tracked_attributes:
            raise AttributeError(name)
        super(Encoder, self).__setattr__(name, value)

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
        bases = tuple(base for base in bases if base is not object)
        if Encoder not in bases:
            bases = bases + (Encoder,)
        tracked_attributes = set()
        for base in bases:
            tracked_attributes.update(
                set(getattr(base, '_tracked_attributes', set())))
        for key, value in list(class_dict.items()):
            if isinstance(value, _TrackedAttribute):
                value.set_attribute_name(key)
                tracked_attributes.add(key)
        class_dict['_tracked_attributes'] = tuple(tracked_attributes)
        return type.__new__(cls, class_name, bases, class_dict)
