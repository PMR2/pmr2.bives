import unittest
import warnings
import json

import zope.component

from pmr2.bives.testing.dummy import DummySession
from pmr2.bives.testing.layer import BIVES_INTEGRATION_LAYER
from pmr2.bives.view import apply_bives_view
from pmr2.bives.view import BiVeSBaseView


class ViewTestCase(unittest.TestCase):
    """
    Test cases for the views.
    """

    layer = BIVES_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.session = DummySession()

    def test_baseview_update(self):
        view = BiVeSBaseView(self.portal, self.portal.REQUEST)
        view.session = self.session

        view.update()
        self.assertEqual(json.loads(self.session.history[0][2]['data']), {
            'files': ['http://nohost/plone'],
            'commands': ['singleCompHierarchyJson'],
        })
