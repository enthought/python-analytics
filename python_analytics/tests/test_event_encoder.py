from __future__ import absolute_import, unicode_literals

import unittest

from six import add_metaclass, text_type

from ..event_encoder import (
    CustomDimension, CustomMetric, Encoder, EventEncoder, NoValue, Parameter)


@add_metaclass(EventEncoder)
class SomeEvent(object):

    required = Parameter('encoded_name', int, required=True)
    not_required = Parameter('other_name', text_type)
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
        self.assertIs(value, NoValue)

    def test_attribute_value(self):
        # Given
        expected = 5
        event = SomeEvent(required=expected)

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
        self.assertIs(value, NoValue)

    def test_custom_dimension_type(self):
        # Given
        event = SomeEvent()

        # When
        with self.assertRaises(TypeError):
            event.custom_dimension = 1

    def test_custom_dimension_valid(self):
        # Given
        expected = 'name'
        event = SomeEvent(custom_dimension=expected)

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
        self.assertIs(value, NoValue)

    def test_custom_metric_type(self):
        # Given
        event = SomeEvent()

        # When
        with self.assertRaises(TypeError):
            event.custom_metric = 'name'

    def test_custom_metric_valid(self):
        # Given
        expected = 2
        event = SomeEvent(custom_metric=expected)

        # When
        value = event.custom_metric

        # Then
        self.assertEqual(value, expected)

    def test_encode_missing_required(self):
        # Given
        event = SomeEvent()

        # When/Then
        with self.assertRaises(ValueError):
            event.encode()

    def test_encode_missing_optional(self):
        # Given
        event = SomeEvent(required=4)
        expected = {'encoded_name': 4}

        # When
        value = event.encode()

        # Then
        self.assertEqual(value, expected)

    def test_encode_all_values(self):
        # Given
        event = SomeEvent(required=4, custom_dimension='thing')
        event.not_required = 'test'
        event.custom_metric = 12
        expected = {'encoded_name': 4,
                    'other_name': 'test',
                    'cd1': 'thing',
                    'cm5': 12}

        # When
        value = event.encode()

        # Then
        self.assertEqual(value, expected)
