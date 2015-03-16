from __future__ import absolute_import, unicode_literals

from .event_encoder import TrackedAttribute, EventEncoder


class Visitor(object, metaclass=EventEncoder):

    user_agent = TrackedAttribute('ua', str, required=False)
    ip_address = TrackedAttribute('uip', str, required=False)

    def __init__(self, user_agent=None, ip_address=None):
        if user_agent is not None:
            self.user_agent = user_agent
        if ip_address is not None:
            self.ip_address = ip_address
