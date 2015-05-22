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

from .interfaces import IBiVeSSimpleForm
from .interfaces import ISettings

registry_prefix = 'pmr2.bives.settings'

logger = logging.getLogger(__name__)


class BiVeSBaseForm(form.PostForm):

    fields = field.Fields(IBiVeSSimpleForm)
    ignoreContext = True

    result_template = ViewPageTemplateFile('bives_simple.pt')

    commands = ['CellML', 'compHierarchyJson', 'reportHtml']

    results = None

    def bives(self, file1, file2):
        data = {
            'files': [file1, file2],
            'commands': self.commands,
        }

        registry = zope.component.getUtility(IRegistry)
        try:
            settings = registry.forInterface(ISettings, prefix=registry_prefix)
        except KeyError:
            self.results = ''
            logger.warning('pmr2.bives add-on may need to be reinstalled.')
            # what about end-user warnings?
            return

        r = requests.post(settings.bives_endpoint, data=json.dumps(data))
        self.results = r.text

    def render(self):
        if not self.results:
            return super(BiVeSBaseForm, self).render()

        return self.result_template()


class BiVeSSimpleForm(BiVeSBaseForm):

    @button.buttonAndHandler(u'Compare', name='compare')
    def compare(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = u'Invalid input'
            return

        # post the data to BiVeS
        self.bives(data['file1'], data['file2'])


class BiVeSFileentryPicker(BiVeSBaseForm):

    template = ViewPageTemplateFile('bives_fileentry_picker.pt')

    @button.buttonAndHandler(u'Compare', name='compare')
    def compare(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = u'Invalid input'
            return

        file1 = self.extractFileentry(data['file1'])
        file2 = self.extractFileentry(data['file2'])

        # post the data to BiVeS
        self.bives(file1, file2)

    def extractFileentry(self, fileentry):
        entry = json.loads(fileentry)
        workspace = self.context.restrictedTraverse(
            str(entry['physical_path']))
        storage = zope.component.getAdapter(workspace, IStorage)
        storage.checkout(entry['rev'])
        return storage.file(entry['file_path'])
