from __future__ import absolute_import, unicode_literals

import unittest

from six import add_metaclass, text_type

from ..event_encoder import (
    CustomDimension, CustomMetric, Encoder, EventEncoder, TrackedAttribute)


@add_metaclass(EventEncoder)
class SomeEvent(object):

    required = TrackedAttribute('encoded_name', int, required=True)
    not_required = TrackedAttribute('other_name', text_type)
    custom_dimension = CustomDimension(1)
    custom_metric = CustomMetric(5)


class TestEventEncoder(unittest.TestCase):

    def test_metaclass_instantiation(self):
        # Given
        event = SomeEvent()

        # Then
        self.assertIsInstance(event, SomeEvent)
        self.assertIsInstance(event, Encoder)
        self.assertIsInstance(event, object)

    def test_type_validation(self):
        # Given
        event = SomeEvent()

        # When/Then
        with self.assertRaises(TypeError):
            event.required = 'non-int'

    def test_missing_required_attribute(self):
        # Given
        event = SomeEvent()

        # When/Then
        with self.assertRaises(ValueError):
            event.required

    def test_missing_non_required_attribute(self):
        # Given
        event = SomeEvent()

        # When
        value = event.not_required

        # Then
        self.assertEqual(value, None)

    def test_attribute_value(self):
        # Given
        event = SomeEvent(required=5)
        expected = ('encoded_name', 5)

        # When
        value = event.required

        # Then
        self.assertEqual(value, expected)

    def test_set_invalid_attribute(self):
        # When/Then
        with self.assertRaises(AttributeError):
            SomeEvent(missing=5)

        # Given
        event = SomeEvent()

        # When/Then
        with self.assertRaises(AttributeError):
            event.missing = 5

    def test_custom_dimension_empty(self):
        # Given
        event = SomeEvent()

        # When
        value = event.custom_dimension

        # Then
        self.assertEqual(value, None)

    def test_custom_dimension_type(self):
        # Given
        event = SomeEvent()

        # When
        with self.assertRaises(TypeError):
            event.custom_dimension = 1

    def test_custom_dimension_valid(self):
        # Given
        event = SomeEvent(custom_dimension='name')
        expected = ('cd1', 'name')

        # When
        value = event.custom_dimension

        # Then
        self.assertEqual(value, expected)

    def test_custom_metric_empty(self):
        # Given
        event = SomeEvent()

        # When
        value = event.custom_metric

        # Then
        self.assertEqual(value, None)

    def test_custom_metric_type(self):
        # Given
        event = SomeEvent()

        # When
        with self.assertRaises(TypeError):
            event.custom_metric = 'name'

    def test_custom_metric_valid(self):
        # Given
        event = SomeEvent(custom_metric=2)
        expected = ('cm5', 2)

        # When
        value = event.custom_metric

        # Then
        self.assertEqual(value, expected)
