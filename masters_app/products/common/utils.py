from django.utils.http import urlencode
from rest_framework.reverse import reverse


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if params:
        url += '?' + urlencode(params)
    return url
