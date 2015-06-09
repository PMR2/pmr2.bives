import zope.component
from zope.interface import implementer

from pmr2.app.exposure.interfaces import IExposureFileTool
from pmr2.app.exposure.interfaces import IExposureFile


@implementer(IExposureFileTool)
class ExposureFileComparisonTool(object):
    """
    Tool for comparing files.
    """

    label = u'Compare...'

    def get_tool_link(self, exposure_object):
        # TODO figure out how to do user-side customization on the type
        # of files that can be added.  Although this might better be
        # done on the comparison page as that is the centralized place
        # for all forms of comparison (i.e. CellML or SBML, etc).

        if IExposureFile.providedBy(exposure_object):
            return exposure_object.absolute_url() + '/bives_pick_file'
