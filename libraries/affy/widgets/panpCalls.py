"""
<name>Present Calls</name>
<description>Calculates differential expression of genes from an eSet object</description>
<tags>Microarray</tags>
<RFunctions>panp:pa.calls</RFunctions>
<icon>readcel.png</icon>
<priority>2010</priority>
"""
from OWRpy import *
import redRGUI
import signals

class panpCalls(OWRpy):

    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, signalManager, "Present Calls", wantMainArea = 0, resizingEnabled = 1)
        
        self.data = None
        self.eset = ''
        self.panpinfo = '' #used to communicate info after session reload.
        
        self.looseCut = '0.02'
        self.tightCut = '0.01'
        self.percentA = '20'
        
        self.saveSettingsList.extend(['data', 'eset', 'panpinfo', 'looseCut', 'tightCut', 'percentA'])
        
        self.setRvariableNames(['PA','PAcalls','PAcalls_sum','Present','peset'])
        

        self.inputs = [("Normalized Eset", signals.affy.REset, self.process)]
        self.outputs = [("Present Gene Signal Matrix", signals.RMatrix), ('PA Calls Fit', signals.RModelFit)]
        
        
        #GUI
        box = redRGUI.widgetBox(self.controlArea, "Options")
        
        self.looseCut = redRGUI.lineEdit(box, label = "Loose Cut", orientation = "horizontal")
        self.looseCut.setText('0.02')
        self.tightCut = redRGUI.lineEdit(box, label = "Tight Cut", orientation = "horizontal")
        self.tightCut.setText('0.01')
        self.percentA = redRGUI.lineEdit(box, label = "Percent Absent", orientation = "horizontal")
        self.percentA.setText('20')
        processbutton = redRGUI.button(self.bottomAreaRight, "Process eSet", callback = self.processEset)
        
        
    def process(self, dataset):
        print 'on procress panp'
        
        if not self.require_librarys(['affy','gcrma','limma','matchprobes','panp']):
            self.status.setText('R Libraries Not Loaded.')
            return

        if dataset == None: 
            self.status.setText("Blank data recieved")
            self.eset = ''
        else:
            print dataset
            self.data = dataset
            self.eset = self.data.getData()
            self.status.setText("Data Received")
            
    def processEset(self):
        if self.eset == '': return
        self.status.setText("Processing Started!!!")
        self.R(self.Rvariables['PA'] + '<-pa.calls('+self.eset+', looseCutoff='+str(self.looseCut.text())+', tightCutoff='+str(self.tightCut.text())+')','setRData', True)
        self.status.setText('PA calls have been calculated')
        
        pafit = signals.RModelFit(data = self.Rvariables['PA'])
        self.rSend('PA Calls Fit', pafit)
        
        
        self.R(self.Rvariables['PAcalls'] + '<-' + self.Rvariables['PA'] + '$Pcalls == "A"','setRData', True)
        self.R(self.Rvariables['PAcalls_sum'] + '<-apply(' + self.Rvariables['PAcalls'] + ', 1, sum)','setRData', True)
        self.R(self.Rvariables['Present'] + '<- ' + self.Rvariables['PAcalls_sum'] + '/length(' + self.Rvariables['PAcalls'] + '[1,]) > '+str(self.percentA.text())+'/100','setRData', True)
        self.R(self.Rvariables['peset']+'<-exprs('+self.eset+')[' + self.Rvariables['Present'] + ',]','setRData',True)
        self.R('colnames('+self.Rvariables['peset']+') <- colnames(exprs('+self.eset+'))')
        self.panpinfo = 'Processed with loose cut off = '+str(self.looseCut.text())+', tight cut off ='+str(self.tightCut.text())+', and percent absent = '+str(self.percentA.text())
        self.status.setText('Processed')
        
        senddata = signals.RMatrix(data = self.Rvariables['peset'])
        self.rSend('Present Gene Signal Matrix', senddata)