"""
<name>Intersect</name>
<description>Shows data in a spreadsheet.</description>
<tags>Data Manipulation</tags>
<RFunctions>base:intersect</RFunctions>
<icon>datatable.png</icon>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses.RVector as rvec
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
class intersect(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["intersect"])
        self.data = {}
         
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs = [("y", rvec.RVector, self.processy),("x", rvec.RVector, self.processx)]
        self.outputs = [("intersect Output", rvec.RVector)]
        
        button(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = "Intersect Output")
        self.resize(500, 200)
    def processy(self, data):
        if data:
            self.RFunctionParam_y=data.getData()
            self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_y = ''
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data.copy()
            self.commitFunction()
        else:
            self.RFunctionParam_x = ''
    def commitFunction(self):
        if str(self.RFunctionParam_y) == '': 
            self.status.setText('No Y data exists')
            return
        if str(self.RFunctionParam_x) == '': 
            self.status.setText('No X data exists')
            return
        self.R(self.Rvariables['intersect']+'<-intersect(y='+str(self.RFunctionParam_y)+',x='+str(self.RFunctionParam_x)+')')
        self.R('txt<-capture.output('+self.Rvariables['intersect']+')')
        
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse =" \n")')
        self.RoutputWindow.insertHtml('<br><br><pre>Shared elements between your inputs:\n'+str(tmp)+'</pre>')        
        newData = rvec.RVector(data = self.Rvariables["intersect"])
        
        self.rSend("intersect Output", newData)
    def getReportText(self, fileDir):
        return 'Sends the intersecting element, those that are the same, in the two incomming data vectors.\n\n'

