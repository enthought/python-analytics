from __future__ import absolute_import, unicode_literals

from six import add_metaclass, text_type

from .event_encoder import TrackedAttribute, EventEncoder


@add_metaclass(EventEncoder)
class Visitor(object):

    user_agent = TrackedAttribute('ua', text_type)
    ip_address = TrackedAttribute('uip', text_type)
