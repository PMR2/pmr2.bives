import json
import requests
import logging

import zope.component
from z3c.form import button
from z3c.form import field
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry

from pmr2.z3cform import form
from pmr2.app.workspace.interfaces import IStorage
from pmr2.app.exposure.interfaces import IExposureSourceAdapter

from Products.CMFCore.utils import getToolByName

from .interfaces import IBiVeSSimpleForm
from .interfaces import ISettings

from .view import BiVeSDiffViewer

registry_prefix = 'pmr2.bives.settings'

logger = logging.getLogger(__name__)


class BiVeSBaseForm(form.PostForm):

    fields = field.Fields(IBiVeSSimpleForm)
    ignoreContext = True

    label = u'BiVeS Model Diff Viewer'

    commands = ['CellML', 'compHierarchyJson', 'reportHtml']

    diff_viewer = BiVeSDiffViewer
    diff_view = None

    session = requests.Session()

    def bives(self, file1, file2, raw_source, raw_target):
        data = {
            'files': [file1, file2],
            'commands': self.commands,
        }

        registry = zope.component.getUtility(IRegistry)
        try:
            settings = registry.forInterface(ISettings, prefix=registry_prefix)
        except KeyError:
            self.status = (u'Could not load settings for pmr2.bives.  Please '
                'check the installation status for this add-on.')
            return

        r = self.session.post(settings.bives_endpoint, data=json.dumps(data))
        try:
            results = r.json()
            # It can be successfully decode so it should be safe(TM)
            results = r.text
        except ValueError:
            results = '{"error": "Server returned unexpected results"}'
        self.diff_view = self.diff_viewer(self.context, self.request)
        self.diff_view.results = results
        self.diff_view.raw_source = raw_source
        self.diff_view.raw_target = raw_target

    def render(self):
        if not self.diff_view:
            return super(BiVeSBaseForm, self).render()

        return self.diff_view()


class BiVeSSimpleForm(BiVeSBaseForm):

    @button.buttonAndHandler(u'Compare', name='compare')
    def compare(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = u'Invalid input'
            return

        # post the data to BiVeS
        self.bives(**data)


class BiVeSFileentryPicker(BiVeSBaseForm):

    template = ViewPageTemplateFile('bives_fileentry_picker.pt')

    @button.buttonAndHandler(u'Compare', name='compare')
    def compare(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = u'Invalid input'
            return

        file1 = self.extractFileentry(data.pop('file1'))
        file2 = self.extractFileentry(data.pop('file2'))

        if file1 is None or file2 is None:
            # TODO make better error message.
            self.status = u'Failed to access all files required.'
            return

        # post the data to BiVeS
        self.bives(file1, file2, **data)

    def extractFileentry(self, fileentry):
        entry = json.loads(fileentry)
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(path={'query': entry['physical_path'], 'depth': 0,})
        if not brains:
            return None

        brain = brains[0]

        try:
            if brain.portal_type == 'Workspace':
                rev = entry['rev']
                path = entry['file_path']
                workspace = brain.getObject()
                storage = zope.component.getAdapter(workspace, IStorage)
                storage.checkout(rev)
            elif brain.portal_type == 'ExposureFile':
                ef = brain.getObject()
                helper = zope.component.getAdapter(ef, IExposureSourceAdapter)
                exposure, w, path = helper.source()
                storage = zope.component.getAdapter(exposure, IStorage)
            else:
                return None

            return storage.file(path)
        except ValueError:
            return None
