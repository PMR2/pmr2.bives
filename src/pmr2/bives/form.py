import json
import requests

import zope.component
from z3c.form import button
from z3c.form import field
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from pmr2.z3cform import form
from pmr2.app.workspace.interfaces import IStorage

from .interfaces import IBiVeSSimpleForm


class BiVeSBaseForm(form.PostForm):

    fields = field.Fields(IBiVeSSimpleForm)
    ignoreContext = True

    result_template = ViewPageTemplateFile('bives_simple.pt')

    bives_endpoint = 'http://localhost:8080/BiVeS-WS-1.3.9.1/'
    commands = ['CellML', 'compHierarchyJson', 'reportHtml']

    results = None

    def bives(self, file1, file2):
        data = {
            'files': [file1, file2],
            'commands': self.commands,
        }

        r = requests.post(self.bives_endpoint, data=json.dumps(data))
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
