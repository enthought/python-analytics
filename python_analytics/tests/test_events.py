from __future__ import absolute_import, unicode_literals

import unittest

from six import text_type

from ..event_encoder import CustomDimension, CustomMetric
from ..events import Event


class TestEvent(unittest.TestCase):

    def test_event_no_label_value(self):
        # Given
        category = 'category'
        action = 'action'
        event = Event(
            category=category, action=action)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_label_no_value(self):
        # Given
        category = 'category'
        action = 'action'
        label = 'an-event-label'
        event = Event(
            category=category, action=action, label=label)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_value_no_label(self):
        # Given
        category = 'category'
        action = 'action'
        value = 42
        event = Event(
            category=category, action=action, value=value)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'ev': value,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_label_value(self):
        # Given
        category = 'category'
        action = 'action'
        label = 'Another event!'
        value = 42
        event = Event(
            category=category, action=action, label=label, value=value)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_dimensions(self):
        # Given
        class MyEvent(Event):
            some_dimension = CustomDimension(1)

        dimension_value = 'some-value'
        category = 'category'
        action = 'action'
        label = 'Another event!'
        value = 42
        event = MyEvent(
            category=category, action=action, label=label, value=value,
            some_dimension=dimension_value)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
            'cd1': dimension_value,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_metrics(self):
        # Given
        class MyEvent(Event):
            some_metric = CustomMetric(5)

        metric_value = 28
        category = 'category'
        action = 'action'
        label = 'Another event!'
        value = 42
        event = MyEvent(
            category=category, action=action, label=label, value=value,
            some_metric=metric_value)
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
            'cm5': metric_value,
        }

        # When
        event_dict = event.encode()

        # Then
        self.assertEqual(event_dict, expected)
