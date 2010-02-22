"""
<name>Data Entry</name>
<description>A table input data entry into a data.frame.</description>
<tags>Data Entry</tags>
<icon>icons/File.png</icon>
<priority>20</priority>

"""

import redRGUI
from OWRpy import *



class dataEntry(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, signalManager, "Data Entry", wantMainArea = 1, resizingEnabled = 1)

        self.rowCount = 10
        self.colCount = 10
        self.maxRow = 0 # sets the most extreme row and cols
        self.maxCol = 0
        self.rowHeaders = True
        self.colHeaders = True

        self.savedData = None
        self.setRvariableNames(['table'])
        
        self.inputs = [('Data Table', RvarClasses.RDataFrame, self.processDF)]
        self.outputs = [('Data Table', RvarClasses.RDataFrame)] # trace problem with outputs
        #GUI.
        
        box = redRGUI.widgetBox(self.controlArea, "Options")
        redRGUI.button(box, self, 'Commit', self.commitTable)
        self.rowcolHeaders = redRGUI.checkBox(box, 'Headers', buttons = ['Row Headers', 'Col Headers'])
        #redRGUI.checkBox(box, 'rowHeaders', 'Use Row Headers:')
        #redRGUI.checkBox(box, 'colHeaders', 'Use Column Headers:')
        #redRGUI.button(box, self, 'Add Column', self.addColumn)
        
        self.splitCanvas = QSplitter(Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)

        
        box = redRGUI.widgetBox(self.controlArea, "Table")
        self.splitCanvas.addWidget(box)
        self.dataTable = redRGUI.table(box, None, self.rowCount+1, self.colCount+1)
        self.dataTable.show()
        # self.setRownamesColor()
        # self.setColnamesColor()
        upcell = QTableWidgetItem()
        upcell.setBackgroundColor(Qt.gray)
        upcell.setFlags(Qt.NoItemFlags) #sets the cell as being unselectable
        self.dataTable.setItem(0,0,upcell)
        # self.dataTable.item(0,0).setBackgroundColor(Qt.gray)
        self.connect(self.dataTable, SIGNAL("cellClicked(int, int)"), self.cellClicked) # works OK
        self.connect(self.dataTable, SIGNAL("cellChanged(int, int)"), self.itemChanged)
        self.resize(800,600)
        
    def processDF(self, data):
        if data:
            self.data = data['data']
            self.savedData = data
            self.populateTable()
        else:
            return
    def populateTable(self):
        self.dataTable.clear()
        rownames = self.R('rownames('+self.data+')')
        rlen = self.R('length('+self.data+'[,1])')
        self.dataTable.setRowCount(rlen+1)
        self.rowCount = rlen+1
        
        print str(rownames)
        if rownames != 'NULL':
            row = 1
            for name in rownames:
                newitem = QTableWidgetItem(str(name))
                self.dataTable.setItem(row,0,newitem)
                row += 1
            self.rowHeaders = True
        clen = self.R('length('+self.data+'[1,])')
        self.colCount = clen+1
        self.dataTable.setColumnCount(clen+1)
        colnames = self.R('colnames('+self.data+')')
        if type(colnames) == type(''):
            colnames = [colnames]
        if colnames != 'NULL':  
            col = 1
            for name in colnames:
                newitem = QTableWidgetItem(str(name))
                self.dataTable.setItem(0, col, newitem)
                col += 1
            self.colHeaders = True
        data = self.R(self.data)
        col = 1
        for name in colnames:
           
            for i in range(1, rlen+1):
                newitem = QTableWidgetItem(str(data[name][i-1])) # must correct for the different indexis of R and python
                self.dataTable.setItem(i, col, newitem)
            col += 1
        upcell = QTableWidgetItem()
        upcell.setBackgroundColor(Qt.gray)
        upcell.setFlags(Qt.NoItemFlags) #sets the cell as being unselectable
        self.dataTable.setItem(0,0,upcell)
        # self.dataTable.item(0,0).setBackgroundColor(Qt.gray)
        self.connect(self.dataTable, SIGNAL("cellClicked(int, int)"), self.cellClicked) # works OK
        self.connect(self.dataTable, SIGNAL("cellChanged(int, int)"), self.itemChanged)
    def cellClicked(self, row, col):
        pass

    def onCellFocus(self, currentRow, currentCol, tb):
        if len(tb) == 0: return
        print 'cell on focus'
        item = tb.item(currentRow, currentCol)
        tb.editItem(item)
    
    def itemChanged(self, row, col):
        if row > self.rowCount-3: #bump up the number of cells to keep up with the needs of the table
            self.dataTable.setRowCount(self.rowCount+3)
            self.rowCount += 3
        if col > self.colCount-3:
            self.dataTable.setColumnCount(self.colCount+3)
            self.colCount += 3
        if row > self.maxRow: self.maxRow = row #update the extremes of the row and cols
        if col > self.maxCol: self.maxCol = col
        self.dataTable.setCurrentCell(row+1, col)


        
    def commitTable(self):
        #run through the table and make the output
        trange = self.dataTable.selectedRanges()[0]
        if trange.leftColumn() == trange.rightColumn() and trange.topRow() == trange.bottomRow():
            rowi = range(0, self.maxRow+1)
            coli = range(0, self.maxCol+1)
        else:

            rowi = range(trange.topRow(), trange.bottomRow()+1)
            coli = range(trange.leftColumn(), trange.rightColumn()+1)
            
        if self.dataTable.item(rowi[0], coli[0]) == None: 

            self.rowHeaders = True
            self.colHeaders = True
        rownames = {}  
        colnames = {}        
        if self.rowHeaders == True:
            
            for i in rowi[1:]:
                item = self.dataTable.item(i, coli[0])
                if item != None:
                    thisText = item.text()
                else: thisText = str(i)
                if thisText == None or thisText == '':
                    thisText = str(i)
                    
                rownames[str(i)] = (str(thisText))
            coli = coli[1:] #index up the cols

        if self.colHeaders == True:
            for j in coli:
                item = self.dataTable.item(rowi[0], j)
                if item != None:
                    thisText = item.text()
                else: thisText = '"'+str(j)+'"'
                if thisText == None or thisText == '':
                    thisText = '"'+str(j)+'"'
                colnames[str(j)] = (str(thisText))
            rowi = rowi[1:] #index up the row count

        rinsertion = []
        
        for j in coli:
            element = ''
            if colnames:
                element += colnames[str(j)]+'='
            element += 'c('
            inserts = []
            for i in rowi:

                tableItem = self.dataTable.item(i,j)
                if tableItem == None:
                    inserts.append('NA')
                else:
                    try: #catch if the element can be coerced to numeric in the table
                        float(tableItem.text()) #will fail if can't be coerced to int 
                        inserts.append(str(tableItem.text()))
                    except:
                        if tableItem.text() == 'NA': 
                            inserts.append(str(tableItem.text()))
                            print 'set NA'
                        elif tableItem.text() == '1.#QNAN': 
                            inserts.append('NA') #if we read in some data
                            print 'set QNAN to NA'
                        else: 
                            inserts.append('"'+str(tableItem.text())+'"')
                            print str(tableItem.text())+' set as text'

            insert = ','.join(inserts)
            element += insert+')'
            rinsertion.append(element)
            
        rinsert = ','.join(rinsertion)

        if len(rownames) > 0:
            rname = []
            for i in rowi:
                rname.append(rownames[str(i)])
            rnf = '","'.join(rname)
            rinsert += ', row.names =c("'+rnf+'")' 
        self.R(self.Rvariables['table']+'<-data.frame('+rinsert+')')

        self.rSend('Data Table', {'data':self.Rvariables['table']})
        self.savedData = {'data':self.Rvariables['table']}
    def onLoadSavedSession(self):
        if self.R('exists("'+self.Rvariables['table']+'")'):
            self.rSend('Data Table', {'data':self.Rvariables['table']})
        self.processDF(self.savedData)
       
            