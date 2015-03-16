from requests.utils import default_user_agent as requests_user_agent

from python_analytics import __version__


def get_user_agent(original):
    if original is None:
        original = requests_user_agent()
    return 'python-analytics/{} {}'.format(__version__, original)
