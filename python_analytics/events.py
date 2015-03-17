from __future__ import absolute_import, unicode_literals

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


class Event(object, metaclass=EventEncoder):

    hit = TrackedAttribute('t', str, required=True)
    category = TrackedAttribute('ec', str, required=True)
    action = TrackedAttribute('ea', str, required=True)
    label = TrackedAttribute('el', str)
    value = TrackedAttribute('ev', int)

    def __init__(self, category, action, label=None, value=None,
                 custom_dimensions=None, custom_metrics=None):
        self.hit = 'event'
        self.category = category
        self.action = action
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value

        if custom_dimensions is None:
            custom_dimensions = ()
        else:
            custom_dimensions = tuple(custom_dimensions)

        if custom_metrics is None:
            custom_metrics = ()
        else:
            custom_metrics = tuple(custom_metrics)

        self._dimensions = custom_dimensions
        self._metrics = custom_metrics

    def to_dict(self):
        value = super(Event, self).to_dict()
        for dimension in self._dimensions:
            value[dimension.key] = dimension.value
        for metric in self._metrics:
            value[metric.key] = metric.value
        return value
