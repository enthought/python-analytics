from __future__ import absolute_import, unicode_literals


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


class Event(object):

    def __init__(self, category, action, label=None, value=None,
                 custom_dimensions=None, custom_metrics=None):
        self.category = category
        self.action = action
        self.label = label
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
        value = {
            't': 'event',
            'ec': self.category,
            'ea': self.action,
        }
        if self.label is not None:
            value['el'] = self.label
        if self.value is not None:
            value['ev'] = self.value
        for dimension in self._dimensions:
            value[dimension.key] = dimension.value
        for metric in self._metrics:
            value[metric.key] = metric.value
        return value
