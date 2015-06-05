import zope.component
from zope.interface import implementer

from pmr2.app.exposure.interfaces import IExposureFileTool


@implementer(IExposureFileTool)
class ExposureFileComparisonTool(object):
    """
    Tool for comparing files.
    """

    label = u'Compare...'

    def get_tool_link(self, exposure_object):
        return exposure_object.absolute_url() + '/bives_pick_file'
