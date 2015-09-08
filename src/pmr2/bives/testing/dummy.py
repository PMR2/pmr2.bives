import json


class DummyResponse(object):
    def __init__(self, raw, status_code=200):
        self.raw = self.text = self.content = raw
        self.status_code = status_code

    def json(self):
        return json.loads(self.raw)


class DummySession(object):

    data = {
        # A valid JSON Object
        'valid': '{"reportHtml": "A Test Report"}',
        # An invalid JSON object, usually from an error response.
        'invalid': '<error></error>',
    }

    def __init__(self, key='valid'):
        self.key = key
        self.history = []

    def post(self, target, *a, **kw):
        self.history.append((target, a, kw))
        return DummyResponse(self.data[self.key])


