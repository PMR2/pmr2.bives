import zope.interface
import zope.schema


class IBiVeSSimpleForm(zope.interface.Interface):
    """
    BiVeS Input Form.
    """

    file1 = zope.schema.TextLine(
        title=u'File1',
        description=u'First file to be compared',
    )

    file2 = zope.schema.TextLine(
        title=u'File2',
        description=u'Second file to be compared',
    )
