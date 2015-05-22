import unittest
import warnings

import zope.component

from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_ID, setRoles

from pmr2.testing.base import TestRequest

from pmr2.bives.testing.layer import BIVES_INTEGRATION_LAYER
from pmr2.bives.interfaces import ISettings


class SettingsTestCase(unittest.TestCase):
    """
    Test that the settings is set up correctly.
    """

    layer = BIVES_INTEGRATION_LAYER

    def setUp(self):
        pass

    def test_basic_settings(self):
        registry = zope.component.getUtility(IRegistry)
        settings = registry.forInterface(ISettings,
            prefix='pmr2.bives.settings')

        self.assertTrue(settings.bives_endpoint.startswith('http://localhost'))
        settings.bives_endpoint = u'http://nohost'
        self.assertEqual(settings.bives_endpoint, u'http://nohost')
