from __future__ import absolute_import, unicode_literals

import unittest

from ..tracker import CustomDimension, CustomMetric, Event


class TestCustomFields(unittest.TestCase):

    def test_custom_dimension(self):
        # Given
        dimension = CustomDimension(1, 42)

        # Then
        self.assertEqual(dimension.key, 'cd1')
        self.assertEqual(dimension.value, 42)

        # Given
        dimension = CustomDimension(2, 'eight')

        # Then
        self.assertEqual(dimension.key, 'cd2')
        self.assertEqual(dimension.value, 'eight')

    def test_custom_metric(self):
        # Given
        dimension = CustomMetric(1, 42)

        # Then
        self.assertEqual(dimension.key, 'cm1')
        self.assertEqual(dimension.value, 42)

        # Given
        dimension = CustomMetric(2, 'eight')

        # Then
        self.assertEqual(dimension.key, 'cm2')
        self.assertEqual(dimension.value, 'eight')


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
        event_dict = event.to_dict()

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
        event_dict = event.to_dict()

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
        event_dict = event.to_dict()

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
        event_dict = event.to_dict()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_dimensions(self):
        # Given
        dimension_value = 'some-value'
        dimension = CustomDimension(1, dimension_value)
        category = 'category'
        action = 'action'
        label = 'Another event!'
        value = 42
        event = Event(
            category=category, action=action, label=label, value=value,
            custom_dimensions=[dimension])
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
            'cd1': dimension_value,
        }

        # When
        event_dict = event.to_dict()

        # Then
        self.assertEqual(event_dict, expected)

    def test_event_metrics(self):
        # Given
        metric_value = 28
        metric = CustomMetric(1, metric_value)
        category = 'category'
        action = 'action'
        label = 'Another event!'
        value = 42
        event = Event(
            category=category, action=action, label=label, value=value,
            custom_metrics=[metric])
        expected = {
            't': 'event',
            'ec': category,
            'ea': action,
            'el': label,
            'ev': value,
            'cm1': metric_value,
        }

        # When
        event_dict = event.to_dict()

        # Then
        self.assertEqual(event_dict, expected)
