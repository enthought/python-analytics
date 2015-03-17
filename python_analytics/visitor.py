from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


@add_metaclass(EventEncoder)
class Visitor(object):

    user_agent = TrackedAttribute('ua', text_type)
    ip_address = TrackedAttribute('uip', text_type)

    def __init__(self, user_agent=None, ip_address=None):
        if user_agent is not None:
            self.user_agent = user_agent
        if ip_address is not None:
            self.ip_address = ip_address
