from pmr2.app.workspace.browser.fileaction import BaseFileAction


class CompareFileAction(BaseFileAction):

    title = u'Compare...'
    description = u'Add this file to the BiVeS model comparison tool.'

    def href(self, view):
        return '/'.join(view._getpath(view='bives_pick_file',
            path=view.data['file']))
