from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class table(widgetState,QTableWidget):
    def __init__(self,widget,data=None, rows = 0, columns = 0, sortable = False, selectionMode = -1, addToLayout = 1):
        QTableWidget.__init__(self,rows,columns,widget)
        self.sortIndex = None
        self.oldSortingIndex = None
        self.data = None
        ### should turn this into a function as all widgets use it to some degree
        if widget and addToLayout and widget.layout():
            widget.layout().addWidget(self)
        elif widget and addToLayout:
            try:
                widget.addWidget(self)
            except: # there seems to be no way to add this widget
                pass
                
        ###
        if selectionMode != -1:
            self.setSelectionMode(selectionMode)
        if data:
            self.setTable(data)
        if sortable:
            self.setSortingEnabled(True)
            self.connect(self.horizontalHeader(), SIGNAL("sectionClicked(int)"), self.sort)
        
    def setTable(self, data):
        print 'in table set'
        if data==None:
            return
        self.data = data
        qApp.setOverrideCursor(Qt.WaitCursor)
        #print data
        self.clear()
        self.setRowCount(len(data[data.keys()[0]]))
        self.setColumnCount(len(data.keys()))

        n = 0
        for key in data:
            m = 0
            for item in data[key]:
                newitem = QTableWidgetItem(str(item))
                self.setItem(m, n, newitem)
                m += 1
            n += 1
        
        qApp.restoreOverrideCursor()

    def sort(self, index):
        if index == self.oldSortingIndex:
            order = self.oldSortingOrder == Qt.AscendingOrder and Qt.DescendingOrder or Qt.AscendingOrder
        else:
            order = Qt.AscendingOrder
        self.oldSortingIndex = index
        self.oldSortingOrder = order
        
    def getSettings(self):
    
        r = {'data': self.data,'selection':[[i.row(),i.column()] for i in self.selectedIndexes()]}
        if self.oldSortingIndex:
            r['sortIndex'] = self.oldSortingIndex
            r['order'] = self.oldSortingOrder
            
        # print r
        return r
    def loadSettings(self,data):
        # print data
        self.setTable(data['data'])
        # print 'start'
        # print data
        if 'sortIndex' in data.keys():
            # print 'aaaaaaaaa###############'
            self.sortByColumn(data['sortIndex'],data['order'])
        print 'aaaaaaaaatable#########################'
        if 'selection' in data.keys() and len(data['selection']):
            # print 'table#########################'
            for i in data['selection']:
                # print i
                self.setItemSelected(self.item(i[0],i[1]),True)
            
                #self.selectRow(i[0])
            
    def delete(self):
        # rows = self.rowCount()
        # columns = self.columnCount()
        # for i in range(0, rows):
            # for j in range(0, columns):
                # try:
                    # item = self.item(i, j)
                    # if type(item) == PyQt4.QtGui.QTableWidgetItem:
                        #print type(item)
                        # sip.delete(item)
                # except: pass
                # try:
                    # widget = self.cellWidget(i, j)
                    # if widget:
                        #print type(widget)
                        # sip.delete(widget)
                # except: pass
                
        sip.delete(self)