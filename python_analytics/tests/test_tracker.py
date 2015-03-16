from __future__ import absolute_import, unicode_literals

import unittest
import uuid

from mock import patch

import requests
import responses
from six.moves.urllib import parse

from ..events import CustomDimension, CustomMetric, Event
from ..tracker import _AnalyticsHandler, Tracker
from ..utils import get_user_agent


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


class TestAnalyticsHandler(unittest.TestCase):

    def test_default_user_agent(self):
        # Given
        handler = _AnalyticsHandler()

        # Then
        user_agent = handler._session.headers['User-Agent']
        self.assertRegexpMatches(user_agent, r'^python-analytics/')
        self.assertEqual(user_agent, get_user_agent(None))

    def test_override_user_agent(self):
        # Given
        session = requests.Session()
        session.headers['User-Agent'] = 'MyAgent/1.0'
        handler = _AnalyticsHandler(session=session)

        # Then
        user_agent = handler._session.headers['User-Agent']
        self.assertRegexpMatches(
            user_agent, r'^python-analytics/[^ ]+ MyAgent/1.0')
        self.assertEqual(user_agent, get_user_agent('MyAgent/1.0'))

    @responses.activate
    def test_send_analytics(self):
        # Given
        responses.add(
            responses.POST,
            _AnalyticsHandler.target,
            status=200,
        )
        uid = str(uuid.uuid4())
        expected = {
            'v': ['1'],
            'tid': ['GA-ID'],
            'cid': [uid],
        }

        handler = _AnalyticsHandler()
        data = {
            'v': 1,
            'tid': 'GA-ID',
            'cid': uid,
        }

        # When
        handler.send(data)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        sent_data = parse.parse_qs(request.body)
        self.assertEqual(sent_data, expected)


class TestTracker(unittest.TestCase):
    maxDiff = None

    @patch('uuid.uuid4')
    @responses.activate
    def test_tracker(self, uuid4):
        # Given
        responses.add(
            responses.POST,
            _AnalyticsHandler.target,
            status=200,
        )

        my_uuid = 'my-uuid'
        uuid4.return_value = my_uuid
        category = 'category'
        action = 'action'
        tracker = Tracker('GA-ID')
        event = Event(category, action)
        expected = {
            'v': ['1'],
            'tid': ['GA-ID'],
            'cid': [my_uuid],
            't': ['event'],
            'ec': [category],
            'ea': [action],
        }

        # When
        tracker.send(event)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        sent_data = parse.parse_qs(request.body)
        self.assertEqual(sent_data, expected)
