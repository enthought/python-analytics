from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
from weakref import WeakKeyDictionary

from six import add_metaclass, text_type


NoValue = object()


@add_metaclass(ABCMeta)
class BaseParameter(object):
    def __init__(self, type_, required):
        self._name = None
        self._required = required
        self._type = type_
        self._data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._get_value(instance, owner)

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
    def format(self, value):
        """Format the key and value for Google Analytics.

        """


class Parameter(BaseParameter):

    def __init__(self, target_name, type_=None, required=False):
        super(Parameter, self).__init__(type_, required)
        self._target_name = target_name

    def format(self, value):
        return (self._target_name, value)


class _CustomParameter(BaseParameter):

    FORMAT = None
    TYPE = None

    def __init__(self, index, required=False):
        super(_CustomParameter, self).__init__(self.TYPE, required)
        self._index = index

    def format(self, value):
        return (self.FORMAT.format(self._index), value)


class CustomDimension(_CustomParameter):

    FORMAT = 'cd{:d}'
    TYPE = text_type


class CustomMetric(_CustomParameter):

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
        type_ = type(self)
        for attribute_name in self._tracked_attributes:
            item = getattr(self, attribute_name)
            if item is NoValue:
                continue
            formatter = getattr(type_, attribute_name)
            key, value = formatter.format(item)
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
            if isinstance(value, BaseParameter):
                value.set_attribute_name(key)
                tracked_attributes.add(key)
        class_dict['_tracked_attributes'] = tuple(tracked_attributes)
        return type.__new__(cls, class_name, bases, class_dict)
