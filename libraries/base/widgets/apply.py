"""
<name>Apply</name>
<author>Anup Parikh (anup@red-r.org) and Kyle R Covington (kyle@red-r.org)</author>
<description>Applies math across a data table.  These functions could include max (maximum value), mean (the mean value), median (median value), etc.>description>
<RFunctions>base:apply</RFunctions>
<tags>Data Manipulation</tags>
<icon>rexecutor.png</icon>
<inputWidgets></inputWidgets>
<outputWidgets>plotting_plot, base_RDataTable, base_ListSelector, base_DataExplorer, base_rowcolPicker, base_rViewer</outputWidgets>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses.RDataFrame as rdf
import libraries.base.signalClasses.RVector as rvec
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.separator import separator
from libraries.base.qtWidgets.Rtable import Rtable
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
class apply(OWRpy): 
    globalSettingsList = ['functions']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["apply"])
        self.data = {}
         
        self.RFunctionParam_X = ''
        self.inputs = [("X", rdf.RDataFrame, self.processX)]
        self.outputs = [("apply Output", rvec.RVector)]
        
        area = widgetBox(self.controlArea,orientation='horizontal')       
        
        box = widgetBox(area)
        box.setMinimumWidth(200)
        area.layout().setAlignment(box,Qt.AlignLeft)
        
        self.functions =  listBox(box,  label = "Select Function",
        items=['mean','median','max','min','sum','log2', 'log10'],callback=self.functionSelect)
        self.functions.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.functions.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding ,QSizePolicy.Expanding ))                
        # box.layout().setStretchFactor(self.functions.hb,4)
        
        separator(box,height=10)
        self.functionText = textEdit(box,label='This function will be applied:')
        
        self.RFunctionParamMARGIN_radioButtons =  radioButtons(box,  
        label = "to:", buttons = ['Rows', 'Columns'],setChecked='Rows',
        orientation='horizontal')
        
        button(box, "Commit", align='right', callback = self.commitFunction)
        
        self.outputTable = Rtable(area,sortable=True)

    def processX(self, data):
        if data:
            self.RFunctionParam_X=data.getData()
            self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_X=''
    def functionSelect(self):
        selection = self.functions.getCurrentSelection()
        self.functionText.setText(selection[0])
    def commitFunction(self):
        func = str(self.functionText.toPlainText())
        if str(self.RFunctionParam_X) == '' or func =='': return

        if not self.functions.findItems(func,Qt.MatchExactly):
            self.functions.addItem(func)
            self.saveGlobalSettings()

        injection = []
        
        if self.RFunctionParamMARGIN_radioButtons.getChecked() == 'Rows':
            string = 'MARGIN='+str(1)
            injection.append(string)
        else:
            string = 'MARGIN = '+str(2)
            injection.append(string)
            
            
        string = 'FUN='+str(self.functionText.toPlainText())
        injection.append(string)

        
        inj = ','.join(injection)
        try:
            self.R(self.Rvariables['apply']+'<-apply(X='+str(self.RFunctionParam_X)+','+inj+')')
        except: 
            return

        
        self.outputTable.setRTable(self.Rvariables['apply'])
        
        newData = rvec.RVector(data = self.Rvariables['apply'])

        self.rSend("apply Output", newData)
        
    def getReportText(self, fileDir):
        return 'Data was manipulated using the apply feature performing the function %s along the %s of the data.\n\n' % (str(self.functionText.toPlainText()), self.RFunctionParamMARGIN_radioButtons.getChecked())
