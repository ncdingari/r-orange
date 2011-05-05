"""
<name>Clipboard</name>
"""
from OWRpy import * 
import redR
from libraries.base.qtWidgets.button import button as redRButton
import libraries.base.signalClasses as signals

class clipboard(OWRpy): 
    settingsList = []
    def __init__(self, **kwargs):
        OWRpy.__init__(self, **kwargs)
        self.RFunctionParam_data = ''
        self.inputs.addInput("data", "Data Table", signals.RDataFrame.RDataFrame, self.processdata)
        
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processdata(self, data):
        if data:
            self.RFunctionParam_data=data.getData()
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': 
            self.status.setText('No data to work with')
            return
        self.R('write.table(%s, "clipboard", sep = \'\\t\', col.names = NA)' % self.RFunctionParam_data, wantType = redR.NOCONVERSION)
        
        
    