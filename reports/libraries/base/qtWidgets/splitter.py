## plitter Widget.  This widget provides a way to resize widgets within a main area.  To keep things working we won't allow widgets to be added to the splitter but will instead return areas into which widgets can be added using the conventional methods.

from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libraries.base.qtWidgets.widgetBox import widgetBox

class splitter(QSplitter, widgetState):
    def __init__(self, widget = None, orientation = 'horizontal'):
        QSplitter.__init__(self, widget)
        
        if widget:
            widget.layout().addWidget(self)
        if orientation == 'horizontal':
            self.setOrientation(Qt.Horizontal)
        else:
            self.setOrientation(Qt.Vertical)
            
    def widgetArea(self, orientation = 'horizontal'):
        newWidgetBox = widgetBox(None, orientation = orientation)
        self.addWidget(newWidgetBox)
        return newWidgetBox
        