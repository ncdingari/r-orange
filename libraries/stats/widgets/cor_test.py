"""
<name>Test For Correlation (Single)</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<RFunctions>stats:cor.test</RFunctions>
<tags>Parametric</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI, signals
import redRGUI 
class cor_test(OWRpy): 
    settingsList = []
    def __init__(self, **kwargs):
        OWRpy.__init__(self, **kwargs)
        self.setRvariableNames(["cor.test"])
        self.data = {}
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'y', signals.base.RVector, self.processy)
        self.inputs.addInput('id1', 'x', signals.base.RVector, self.processx)

        redRGUI.base.commitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRGUI.base.textEdit(self.controlArea, label = "RoutputWindow")
    def processy(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_y=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def processx(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        inj = ','.join(injection)
        self.R(self.Rvariables['cor.test']+'<-cor.test(y=as.numeric(as.character('+unicode(self.RFunctionParam_y)+')),x=as.numeric(as.character('+unicode(self.RFunctionParam_x)+')),'+','+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['cor.test']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
