import unittest
import warnings
import json

import zope.component

from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_ID, setRoles

from pmr2.testing.base import TestRequest

from pmr2.bives.testing.layer import BIVES_INTEGRATION_LAYER
from pmr2.bives.interfaces import ISettings
from pmr2.bives.form import BiVeSBaseForm
from pmr2.bives.form import BiVeSFileentryPicker


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


class FormTestCase(unittest.TestCase):
    """
    Test cases for the forms, where applicable.
    """

    layer = BIVES_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.session = DummySession()

    def test_basic_render(self):
        form = BiVeSBaseForm(self.portal, self.portal.REQUEST)
        form.update()
        result = form.render()
        self.assertIn('form.widgets.file1', result)

    def test_call_bives_standard(self):
        form = BiVeSBaseForm(self.portal, self.portal.REQUEST)
        form.session = self.session
        form.bives('file1', 'file2')
        self.assertEqual(json.loads(self.session.history[0][2]['data']), {
            'files': ['file1', 'file2'],
            'commands': ['CellML', 'compHierarchyJson', 'reportHtml'],
        })
        result = form.render()
        self.assertIn('data = {"reportHtml": "A Test Report"}', result)

    def test_call_bives_error(self):
        form = BiVeSBaseForm(self.portal, self.portal.REQUEST)
        self.session.key = 'invalid'
        form.session = self.session
        form.bives('file1', 'file2')
        self.assertEqual(json.loads(self.session.history[0][2]['data']), {
            'files': ['file1', 'file2'],
            'commands': ['CellML', 'compHierarchyJson', 'reportHtml'],
        })
        result = form.render()
        self.assertIn('data = {"error": "Server returned unexpected results"}',
            result)

    def test_extract_fileentry_no_such_path(self):
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        results = form.extractFileentry('{"physical_path": "/no/such/path", '
            '"rev": "abcdef", "file_path": "/to/testfile"}')
        self.assertIsNone(results)

    def test_extract_fileentry(self):
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        results = form.extractFileentry(
            '{"physical_path": "/plone/workspace/test", '
            '"rev": "1", "file_path": "file3"}')
        self.assertEqual(results, 'A new test file.\n')

    def test_extract_fileentry_compare(self):
        self.portal.REQUEST.method = 'POST'
        self.portal.REQUEST.form = {
            'form.widgets.file1': '{"physical_path": "/plone/workspace/test", '
                '"rev": "1", "file_path": "file3"}',
            'form.widgets.file2': '{"physical_path": "/plone/workspace/test", '
                '"rev": "2", "file_path": "file3"}',
            'form.buttons.compare': 1,
        }
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        form.disableAuthenticator = True
        form.session = self.session
        result = form()
        self.assertIn('var data = {"reportHtml": "A Test Report"}', result)
        self.assertEqual(self.session.history[0][0],
            u'http://localhost:8080/BiVeS-WS-1.3.9.1/')
        self.assertEqual(json.loads(self.session.history[0][2]['data']), {
            "files": ["A new test file.\n", "Yes file1 is removed\n"],
            "commands": ["CellML", "compHierarchyJson", "reportHtml"]
        })

    def test_extract_fileentry_compare_objpathfail(self):
        self.portal.REQUEST.method = 'POST'
        self.portal.REQUEST.form = {
            'form.widgets.file1': '{"physical_path": "/plone/workspace/test", '
                '"rev": "1", "file_path": "file3"}',
            'form.widgets.file2': '{"physical_path": "/plone/w/nosuchthing", '
                '"rev": "2", "file_path": "/no/such/path"}',
            'form.buttons.compare': 1,
        }
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        form.disableAuthenticator = True
        form.session = self.session
        result = form()
        self.assertEqual(form.status, 'Failed to access all files required.')

    def test_extract_fileentry_compare_storagepathfail(self):
        self.portal.REQUEST.method = 'POST'
        self.portal.REQUEST.form = {
            'form.widgets.file1': '{"physical_path": "/plone/workspace/test", '
                '"rev": "1", "file_path": "file3"}',
            'form.widgets.file2': '{"physical_path": "/plone/workspace/test", '
                '"rev": "2", "file_path": "/no/such/path"}',
            'form.buttons.compare': 1,
        }
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        form.disableAuthenticator = True
        form.session = self.session
        result = form()
        self.assertEqual(form.status, 'Failed to access all files required.')

    def test_extract_fileentry_compare_storagerevfail(self):
        self.portal.REQUEST.method = 'POST'
        self.portal.REQUEST.form = {
            'form.widgets.file1': '{"physical_path": "/plone/workspace/test", '
                '"rev": "1", "file_path": "file3"}',
            'form.widgets.file2': '{"physical_path": "/plone/workspace/test", '
                '"rev": "no such rev", "file_path": "file3"}',
            'form.buttons.compare': 1,
        }
        form = BiVeSFileentryPicker(self.portal, self.portal.REQUEST)
        form.disableAuthenticator = True
        form.session = self.session
        result = form()
        self.assertEqual(form.status, 'Failed to access all files required.')
