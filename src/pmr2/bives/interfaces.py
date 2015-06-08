import zope.interface
import zope.schema


class IBiVeSSimpleForm(zope.interface.Interface):
    """
    BiVeS Input Form.
    """

    raw_source = zope.schema.TextLine(
        title=u'Raw source',
        description=u'',
    )

    raw_target = zope.schema.TextLine(
        title=u'Raw target',
        description=u'',
    )

    file1 = zope.schema.TextLine(
        title=u'File1',
        description=u'First file to be compared',
    )

    file2 = zope.schema.TextLine(
        title=u'File2',
        description=u'Second file to be compared',
    )


class ISettings(zope.interface.Interface):

    bives_endpoint = zope.schema.TextLine(
        title=u'BiVeS WS (webservice) endpoint',
        description=u'The webservice endpoint for BiVeS.',
        required=False,
    )
