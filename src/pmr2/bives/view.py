import json
import requests

import zope.component
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry

from pmr2.z3cform.page import SimplePage
from pmr2.app.workspace.browser.browser import FilePage

from .interfaces import ISettings

registry_prefix = 'pmr2.bives.settings'


def apply_bives_view(view, files, commands, attributes):
    data = {
        'files': files,
        'commands': commands,
    }

    registry = zope.component.getUtility(IRegistry)
    try:
        settings = registry.forInterface(ISettings, prefix=registry_prefix)
    except KeyError:
        view.status = (u'Could not load settings for pmr2.bives.  Please '
            'check the installation status for this add-on.')
        return

    try:
        r = view.session.post(settings.bives_endpoint, data=json.dumps(data))
        results = r.json()
        # It can be successfully decode so it should be safe(TM)
        results = r.text
    except ValueError:
        results = '{"error": "Server returned unexpected results"}'
    except requests.exceptions.ConnectionError:
        results = '{"error": "Error connecting to BiVeS server."}'
    except requests.exceptions.RequestException:
        results = '{"error": "Unexpected exception when handling BiVeS."}'
    view.diff_view = view.diff_viewer(view.context, view.request)
    view.diff_view.results = results

    for k, v in attributes.items():
        setattr(view.diff_view, k, v)


class BiVeSExposurePickFilePage(SimplePage):
    template = ViewPageTemplateFile('bives_exposure_pick_file.pt')
    label = ''

    def physical_path(self):
        return '/'.join(self.context.getPhysicalPath())


class BiVeSWorkspacePickFilePage(FilePage):
    template = ViewPageTemplateFile('bives_workspace_pick_file.pt')
    label = ''

    def physical_path(self):
        return '/'.join(self.context.getPhysicalPath())


class BiVeSDiffViewer(SimplePage):
    template = ViewPageTemplateFile('bives_simple_diff.pt')

    label = u'BiVeS Model Diff Viewer'
    results = None

    raw_source = None
    raw_target = None
