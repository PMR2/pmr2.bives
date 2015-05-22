from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.testing import z2

from pmr2.app.workspace.tests import layer


class BivesLayer(PloneSandboxLayer):

    defaultBases = (layer.WORKSPACE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import pmr2.bives
        self.loadZCML(package=pmr2.bives)
        z2.installProduct(app, 'pmr2.bives')

    def setUpPloneSite(self, portal):
        # install pmr2.bives
        self.applyProfile(portal, 'pmr2.bives:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'pmr2.bives')


BIVES_FIXTURE = BivesLayer()

BIVES_INTEGRATION_LAYER = IntegrationTesting(
    bases=(BIVES_FIXTURE,), name="pmr2.bives:integration")
