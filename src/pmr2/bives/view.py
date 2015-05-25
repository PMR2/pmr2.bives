from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from pmr2.z3cform.page import SimplePage
from pmr2.app.workspace.browser.browser import FilePage


class BiVeSWorkspaceFilePage(FilePage):
    template = ViewPageTemplateFile('bives_workspace_file.pt')
    label = ''

    def physical_path(self):
        return '/'.join(self.context.getPhysicalPath())


class BiVeSDiffViewer(SimplePage):
    template = ViewPageTemplateFile('bives_simple.pt')

    label = u'BiVeS Model Diff Viewer'
    results = None
