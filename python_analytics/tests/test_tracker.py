from __future__ import absolute_import, unicode_literals

import unittest
import uuid

from mock import patch

import requests
import responses
from six.moves.urllib import parse

from ..events import Event
from ..tracker import _AnalyticsHandler, Tracker
from ..utils import get_user_agent


class TestAnalyticsHandler(unittest.TestCase):

    def test_default_user_agent(self):
        # Given
        handler = _AnalyticsHandler()

        # Then
        user_agent = handler._session.headers['User-Agent']
        self.assertRegex(user_agent, r'^python-analytics/')
        self.assertEqual(user_agent, get_user_agent(None))

    def test_override_user_agent(self):
        # Given
        session = requests.Session()
        session.headers['User-Agent'] = 'MyAgent/1.0'
        handler = _AnalyticsHandler(session=session)

        # Then
        user_agent = handler._session.headers['User-Agent']
        self.assertRegex(
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
        event = Event(category=category, action=action)
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
