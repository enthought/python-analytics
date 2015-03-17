from __future__ import absolute_import, unicode_literals

import requests
import uuid

from six import add_metaclass, text_type, PY2
from six.moves.urllib import parse

from .event_encoder import Parameter, EventEncoder
from .utils import get_user_agent


def _encode(item):
    if isinstance(item, text_type):
        return item.encode('utf-8')
    return item


class _AnalyticsHandler(object):

    target = 'https://ssl.google-analytics.com/collect'

    def __init__(self, session=None):
        if session is None:
            session = requests.Session()

        session.headers['User-Agent'] = get_user_agent(
            session.headers.get('User-Agent'))

        self._session = session

    def send(self, data):
        if PY2:
            data = [(_encode(key), _encode(value))
                    for key, value in data.items()]
            encoded_data = parse.urlencode(data)
        else:
            encoded_data = parse.urlencode(data, encoding='utf-8')
        response = self._session.post(self.target, data=encoded_data)
        response.raise_for_status()


@add_metaclass(EventEncoder)
class Tracker(object):

    version = Parameter('v', int)
    tracking_id = Parameter('tid', text_type)
    client_id = Parameter('cid', text_type)

    def __init__(self, tracking_id, client_id=None, requests_session=None):
        if client_id is None:
            client_id = text_type(uuid.uuid4())
        super(Tracker, self).__init__(
            version=1,
            tracking_id=tracking_id,
            client_id=client_id,
        )
        handler = _AnalyticsHandler(session=requests_session)
        object.__setattr__(self, '_handler', handler)

    def send(self, *event_parts):
        """Construct the Universal Analytics request and send it upstream.

        This accepts one or more python-analytics-derived event types,
        and uses the union of all data as a single analytics request.
        This can be used to create separate Visitor and Server
        information types used to augment an Event.

        """
        data = self.to_dict()
        for event in event_parts:
            data.update(event.to_dict())
        self._handler.send(data)
