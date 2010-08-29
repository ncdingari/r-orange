"""
<name>Transpose</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Transposes a data table and sends.</description>
<tags>Data Manipulation</tags>
<RFunctions>utils:t</RFunctions>
<icon>rexecutor.png</icon>
<priority>2040</priority>
"""
from OWRpy import * 

from  libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix

from libraries.base.qtWidgets.button import button
class t(OWRpy): 
    settingsList = ['sentItems']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["t"])
        self.RFunctionParam_x = ''
        self.data={}
        
        
        self.inputs.addInput('id0', 'Input Data Table or Matrix', [redRRDataFrame, redRRMatrix], self.processx)

        self.outputs.addOutput('id0', 'Transposed Data Table', redRRDataFrame)

        
        #box = widgetBox(self.controlArea, "Widget Box")
        button(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            self.data = data
            self.commitFunction()
    def commitFunction(self):
        if self.x == '': return
        
        self.R(self.Rvariables['t']+'<-as.data.frame(t(x='+str(self.RFunctionParam_x)+'))')
        
        newData = redRRDataFrame(data = self.Rvariables['t'])
        newData.dictAttrs = self.data.dictAttrs.copy()
        self.rSend("id0", newData)
    def getReportText(self, fileDir):
        text = 'Data transposed and sent to downstream widgets.\n\n'
        return text