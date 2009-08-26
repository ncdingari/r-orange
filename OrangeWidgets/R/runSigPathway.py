"""
<name>Sig Pathway</name>
<description>Performs Pathway Analysis on a genelist or subset (must specify gene list as either a full list or a subset on connecting)</description>
<icon>icons/readcel.png</icons>
<priority>2030</priority>
"""

import os, glob
import OWGUI
from OWRpy import *
from rpy_options import set_options
set_options(RHOME=os.environ['RPATH'])
import rpy

class runSigPathway(OWRpy):
    settingsList = ['vs', 'Rvariables', 'newdata', 'subtable', 'pAnnots', 'table1', 'table2']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, signalManager, "File", wantMainArea = 1, resizingEnabled = 1)
        
        self.inputs = [("Expression Set", RvarClasses.RDataFrame, self.process), ("Pathway Annotation List", RvarClasses.RDataFrame, self.processPathAnnot), ('Phenotype Vector', RvarClasses.RVector, self.phenotypeConnected)]
        self.outputs = [("Pathway Analysis File", RvarClasses.RDataFrame), ("Pathway Annotation List", RvarClasses.RDataFrame), ("Pathway List", RvarClasses.RDataFrame)]
        
        self.vs = self.variable_suffix
        self.setRvariableNames(['data', 'affy', 'pAnnots', 'chiptype', 'sublist', 'wd', 'minNPS', 'maxNPS', 'phenotype', 'weightType'])
        self.Rpannot = None
        self.data = ''
        self.affy = ''
        self.pAnnots = ''
        self.chiptype = ''
        self.sublist = ''
        self.wd = ''
        self.rand = 'test'
        self.availablePaths = []
        self.minNPS = str(20)
        self.maxNPS = str(500)
        self.phenotype = ''
        self.weightType = 'constant'
        self.newdata = ''
        self.dboptions = ''
        self.subtable = ''
        self.table1 = QTableWidget() # change the table while processing
        self.table2 = QTableWidget() #change the table while processing
        self.loadSettings()
        
        self.usedb = 1
        
        self.require_librarys(['sigPathway'])
        
        #self.sendMe()
        #GUI
        info = OWGUI.widgetBox(self.controlArea, "Info")
        
        self.infoa = OWGUI.widgetLabel(info, "No data connected yet.")
        self.infob = OWGUI.widgetLabel(info, '')
        self.infoc = OWGUI.widgetLabel(info, '')
        
        
        sigPathOptions = OWGUI.widgetBox(self.controlArea, "Options")
        self.pAnnotlist = OWGUI.comboBox(sigPathOptions, self, "Rpannot", label = "Pathway Annotation File:", items = []) #Gets the availiable pathway annotation files.
        self.pAnnotlist.setEnabled(False)
        self.getNewAnnotButton = OWGUI.button(sigPathOptions, self, label = "New Annotation File", callback = self.noFile, width = 200)
        OWGUI.button(sigPathOptions, self, label='Load pathway file', callback = self.loadpAnnot, width = 200)
        OWGUI.button(sigPathOptions, self, 'Run', callback = self.runPath, width = 200)
        OWGUI.button(sigPathOptions, self, 'Show Table', callback = self.tableShow, width = 200)
        OWGUI.checkBox(sigPathOptions, self, 'usedb', 'Use Annotation Database')
        
        #split the canvas into two halves
        self.splitCanvas = QSplitter(Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)
        
        self.pathtable = OWGUI.widgetBox(self, "Pathway Info")
        self.splitCanvas.addWidget(self.pathtable)
        
        self.splitCanvas.addWidget(self.table1)
        self.splitCanvas.addWidget(self.table2)
        

        
        
    def loadpAnnot(self):
        self.rsession('load(choose.files())')
        self.pAnnots = 'G'
        # ## give some output as to what file the annotations are comming from
    def setFileFolder(self):
        self.wd = self.rsession('choose.dir()')
    
    def process(self, data): #collect a preprocessed file for pathway analysis
        if data:
            self.olddata = data
            self.data = data['data']
            self.pAnnotlist.setEnabled(True)
            self.infoa.setText("Data connected")
            self.chiptype = ''
            if 'eset' in data:
                self.affy = data['eset']
                self.chiptype = self.rsession('annotation('+self.affy+')')
                self.getChiptype()
            elif 'affy' in data:
                self.affy = data['affy']
                self.chiptype = self.rsession('annotation('+self.affy+')')
                self.getChiptype()
            else:
                self.infob.setText("No Chip Type Info Available")
            if self.chiptype != '':
                self.infob.setText('Your chip type is '+self.chiptype)
            if 'classes' in self.olddata:
                self.phenotype = self.olddata['classes']
            else: return
                #self.rsession('data.entry(colnames('+self.data+'), cla'+self.vs+'=NULL)')
                #self.phenotype = 'cla'+self.vs
        else: return
    def processPathAnnot(self, data): #connect a processed annotation file if removed, re-enable the choose file function
        if data:
            self.pAnnots = data['data']
            self.pAnnotlist.setEnabled(False)
        else: 
            self.pAnnotlist.setEnabled(True)
            self.wdline.setEnabled(True)
            self.wdfilebutton.setEnabled(True)
    def getChiptype(self):
        if self.usedb == 1:
            try:
                self.require_librarys([self.chiptype])
                self.dboptions = ',annotpkg = "'+self.chiptype+'"'
                self.infob.setText("Chip type loaded")
            except:	
                self.infob.setText("There was an exception")
                self.noDbFile() #try to get the db file
        else: return
    
    def noFile(self):
        self.rsession('shell.exec("http://chip.org/~ppark/Supplements/PNAS05.html")') #open website for more pathways
        self.infoa.setText("Please select the file that coresponds to your array type and save to the Pathway Folder in My Documents.") #send the user a message to download the appropriate pathway.
        self.infob.setText("Once you have saved the array please press the update button.") #prompt the user to update the pathway list
        
    def updatePaths(self):
        if self.wd == '':
            self.infob.setText("You must specify a working directory!")
        else:
            try:
                olddir = os.getcwd()
                os.chdir(self.wd)
                self.pAnnotlist.clear()
                self.pAnnotlist.addItems(glob.glob("*.RData"))
                os.chdir(olddir)
            except:
                self.infob.setText("There was a problem accessing your directory, please confirm that it is correct.")
        
    def noDbFile(self):
        try:
            self.rsession('source("http://bioconductor.org/biocLite.R")')
            self.rsession('biocLite("'+self.chiptype+'")')
            self.rsession('biocLite("'+self.chiptype+'.db")')
            self.require_librarys([self.chiptype])
            #r('require("'+self.chiptype+'")')
            #r('require("'+self.chiptype+'.db")')
            self.infob.setText("Chip type downloaded and loaded")
            self.dboptions = ',annotpkg = "'+self.chiptype+'"'
        except: 
            self.infoa.setText("Unable to include the .db file, please check that you are connected to the internet and that your .db file is available.")
            self.infob.setText("Your chip type appears to be "+self.chiptype+".")
            self.dboptions = ''
            

        
    def runPath(self):
        self.rsession('sigpath_'+self.rand+'<-runSigPathway('+self.pAnnots+', minNPS='+self.minNPS+', maxNPS = '+self.maxNPS+', '+self.data+', phenotype = '+self.phenotype+', weightType = "'+self.weightType+'"'+self.dboptions+')')
        self.newdata = self.olddata.copy()
        self.newdata['data'] = 'sigpath_'+self.rand+'$df.pathways'
        self.newdata['sigPathObj'] = 'sigpath_'+self.rand
        self.send("Pathway Analysis File", self.newdata)
        
        #make the table to show the results, should be interactive and send an object containing the subset to the pathway list
        # self.tstruct = self.newdata['data']
        # self.createTable()
        headers = r('colnames('+self.newdata['data']+')')
        #self.headers = r('colnames('+self.dataframename+')')
        dataframe = r(self.newdata['data'])
        self.table1.setColumnCount(len(headers))
        self.table1.setRowCount(len(dataframe[headers[0]]))
        n=0
        for key in headers:
            m=0
            for item in dataframe[key]:
                newitem = QTableWidgetItem(str(item))
                self.table1.setItem(m,n,newitem)
                m += 1
            n += 1
        self.table1.setHorizontalHeaderLabels(headers)
        self.connect(self.table1, SIGNAL("itemClicked(QTableWidgetItem*)"), self.cellClicked)
        
    def createTable(self):
        try: self.table
        except: pass
        else: self.table.hide()
        self.table = MyTable(self.tstruct)  #This section of code is really messy, clean once working properly
        
        self.tableShow()
    
    def tableShow(self):
        try:
            self.table1.show()
            #self.table.setMinimumSize(500, 500)
            self.connect(self.table, SIGNAL("itemClicked(QTableWidgetItem*)"), self.cellClicked)
        except: return
    
        
    def cellClicked(self, item):
        self.clickedRow = int(item.row())+1
        self.subtable = {'data':'sigpath_'+self.rand+'$list.gPS[['+str(self.clickedRow)+']]'}
        self.sendMe()
        try: self.table2
        except: pass
        else: self.table2.clear()
        #self.table2 = MyTable(self.subtable['data'])
        
        headers = r('colnames('+self.subtable['data']+')')
        #self.headers = r('colnames('+self.dataframename+')')
        dataframe = r(self.subtable['data'])
        self.table2.setColumnCount(len(headers))
        self.table2.setRowCount(len(dataframe[headers[0]]))
        n=0
        for key in headers:
            m=0
            for item in dataframe[key]:
                newitem = QTableWidgetItem(str(item))
                self.table2.setItem(m,n,newitem)
                m += 1
            n += 1
        self.table2.setHorizontalHeaderLabels(headers)
        self.connect(self.table2, SIGNAL("itemClicked(QTableWidgetItem*)"), self.geneClicked)
    
    def geneClicked(self, item):
        
        clickedGene = int(item.row())+1
        if 'GeneID' in self.rsession('colnames(sigpath_'+self.rand+'$list.gPS[['+str(self.clickedRow)+']])'):
            genenumber = self.rsession('sigpath_'+self.rand+'$list.gPS[['+str(self.clickedRow)+']]['+str(clickedGene)+',3]')
            self.rsession('shell.exec("http://www.ncbi.nlm.nih.gov/gene/'+str(genenumber)+'")')
        
    def phenotypeConnected(self, data):
        if data:
            self.phenotype = data['data']
        else: return
    
    def sendMe(self):
        self.send("Pathway Analysis File", self.newdata)
        self.send("Pathway List", self.subtable)
        
                
# from rpy_options import set_options
# set_options(RHOME=os.environ['RPATH'])
# from rpy import *
# from OWWidget import *
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *

# class MyTable(QTableWidget):
    # def __init__(self, dataframe, *args):
        # QTableWidget.__init__(self, *args)
        # self.dataframename = dataframe
        # self.headers = r('colnames('+self.dataframename+')')
        # self.dataframe = r(self.dataframename)
        # self.setColumnCount(len(self.headers))
        # self.setRowCount(len(self.dataframe[self.headers[0]]))
        # n=0
        # for key in self.headers:
            # m=0
            # for item in self.dataframe[key]:
                # newitem = QTableWidgetItem(str(item))
                # self.setItem(m,n,newitem)
                # m += 1
            # n += 1
        # self.setHorizontalHeaderLabels(self.headers)
