from __future__ import absolute_import, unicode_literals

import unittest

from ..tracker import CustomDimension, CustomMetric


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
