==================
 Python Analytics
==================


A very basic client library for server-side Google Universal Analytics
collection.


Basic Usage
===========

Currently ``python-analytics`` only supports sending the ``event`` hit
type to Google Analytics.  There are no plans at this stage to extend
it beyond this.

In the most basic case where there are no custom dimensions or metrics
defined, the provided types may be used directly::

    >>> from python_analytics import Tracker, Event
    >>> tracker = Tracker('GA-ID')
    >>> event = Event(category='my-category', action='an-action', label='An Item', value=1)
    >>> tracker.send(event)


If custom dimensions or metrics are required, a subclass of event is
required to provide developer-readable symbolic names for the custom
attributes::

    >>> from python_analytics import Tracker, Event, CustomDimension, CustomMetric
    >>> tracker = Tracker('GA-ID')
    >>> class DownloadEvent(Event):
    ...     filename = CustomDimension(1)
    ...     target_architecture = CustomDimension(2)
    ...     file_size = CustomMetric(1)
    ...
    >>> event = DownloadEvent(
    ...     category='downloads',
    ...     action='download-installer',
    ...     filename='installer.msi',
    ...     target_architecture='x86_64',
    ...     file_size=14322978,
    ... )
    # This handles encoding the custom dimensions as expected
    >>> print(event.encode())
    {'cd2': 'x86_64', 'cm1': 14322978, 'cd1': 'installer.msi',
     'ea': 'download-installer', 't': 'event', 'ec': 'downloads'}
    >>> tracker.send(event)
