from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from pmr2.z3cform.page import SimplePage
from pmr2.app.workspace.browser.browser import FilePage


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
