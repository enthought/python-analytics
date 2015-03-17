from __future__ import absolute_import, unicode_literals

import unittest

from six import add_metaclass, text_type

from ..event_encoder import EventEncoder, TrackedAttribute


@add_metaclass(EventEncoder)
class SomeEvent(object):

    required = TrackedAttribute('encoded_name', int, required=True)
    not_required = TrackedAttribute('other_name', text_type)


class TestEventEncoder(unittest.TestCase):

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
