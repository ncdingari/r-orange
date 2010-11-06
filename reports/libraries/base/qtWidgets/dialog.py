### custom message dialog that is called with exex_ (a Qt funciton).  This dialog will take any redRGUI qtwidget as its child.
from redRGUI import widgetState

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class dialog(QDialog,widgetState):
    def __init__(self, parent = None, 
    layout = 'vertical',title=None, callback = None):
        widgetState.__init__(self, 'dialog',includeInReports=True)
        QDialog.__init__(self,parent)
        
        if title:
            self.setWindowTitle(title)
        if layout == 'horizontal':
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        if callback:
            QObject.connect(self, SIGNAL('accepted()'), callback)
            QObject.connect(self, SIGNAL('rejected()'), callback)