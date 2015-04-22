import json
import requests

from z3c.form import button
from z3c.form import field
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from pmr2.z3cform import form

from .interfaces import IBiVeSSimpleForm


class BiVeSSimpleForm(form.PostForm):

    fields = field.Fields(IBiVeSSimpleForm)
    ignoreContext = True

    result_template = ViewPageTemplateFile('bives_simple.pt')

    bives_endpoint = 'http://localhost:8080/BiVeS-WS-1.3.9.1/'
    commands = ['CellML', 'compHierarchyJson', 'reportHtml']

    results = None

    @button.buttonAndHandler(u'Compare', name='compare')
    def compare(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = u'Invalid input'
            return

        # post the data to BiVeS

        data = {
            'files': [
                data['file1'],
                data['file2'],
            ],
            'commands': self.commands,
        }

        r = requests.post(self.bives_endpoint, data=json.dumps(data))
        self.results = r.text

    def render(self):
        if not self.results:
            return super(BiVeSSimpleForm, self).render()

        return self.result_template()
