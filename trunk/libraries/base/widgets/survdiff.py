"""
<name>Survival Difference</name>
<description>Calculates the survival differece between groups given a data table with event times, event status, and groupings.  This can perform complex comparisons including interactions.  The parameter rho can be set between 0 and 1 with With rho = 0 this is the log-rank or Mantel-Haenszel test, and with rho = 1 it is equivalent to the Peto & Peto modification of the Gehan-Wilcoxon test.</description>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<RFunctions>survival:survdiff</RFunctions>
<tags>Survival</tags>
<icon>icons/survival.png</icon>
"""
from OWRpy import * 
import redRGUI 
import SurvivalClasses
class survdiff(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, signalManager, "Survival Difference", wantMainArea = 0, resizingEnabled = 1)
        self.setRvariableNames(["survdiff"])
        self.data = None
        self.formula = ''
         
        self.RFunctionParam_data = ''
        self.inputs = [("data", signals.RVariable, self.processdata)]
        self.outputs = [("survdiff Output", signals.RSurvFit)]
        
        self.help.setHtml('<small>Calculates the survival differece between groups given a data table with event times, event status, and groupings.  This can perform complex comparisons including interactions.  The parameter rho can be set between 0 and 1 with With rho = 0 this is the log-rank or Mantel-Haenszel test, and with rho = 1 it is equivalent to the Peto & Peto modification of the Gehan-Wilcoxon test.</small>')
        hbox = redRGUI.widgetBox(self.controlArea, orientation = 'horizontal')
        lbox = redRGUI.widgetBox(hbox)

        self.standardTab = redRGUI.widgetBox(lbox)
        self.RFunctionParamformula =  redRGUI.RFormulaEntry(lbox)
        self.survTime = redRGUI.comboBox(self.RFunctionParamformula.extrasBox, label = 'Time')
        self.RFunctionParamrho_lineEdit =  redRGUI.lineEdit(self.standardTab,  label = "rho:", text = '0', toolTip = 'Sets the rho parameter of the comparison.\nWith rho = 0 this is the log-rank or Mantel-Haenszel test,\nand with rho = 1 it is equivalent to the Peto & Peto modification of the Gehan-Wilcoxon test.')
        redRGUI.button(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRGUI.textEdit(hbox, label = "RoutputWindow")
    def processdata(self, data):
        self.require_librarys(["survival"]) 
        if data:
            self.RFunctionParam_data=data.getData()
            self.data = data
            colnames = self.R('colnames('+self.RFunctionParam_data+')')
            self.RFunctionParamformula.update(self.R('colnames('+self.RFunctionParam_data+')'))
            self.survTime.update(colnames)
            self.commitFunction()
    def commitFunction(self):
        if str(self.RFunctionParam_data) == '': return
        if str(self.survTime.currentText())== '': return
        formulaOutput = self.RFunctionParamformula.Formula()
        if not formulaOutput: return
        if str(self.survTime.currentText()) == formulaOutput[0]: return
        if formulaOutput[0] == '' or formulaOutput[1] =='': return
        injection = []
        injection.append('formula = Surv('+str(self.survTime.currentText())+','+formulaOutput[0]+')~'+formulaOutput[1])
        self.formula = 'formula = Surv('+str(self.survTime.currentText())+','+formulaOutput[0]+')~'+formulaOutput[1]
        if str(self.RFunctionParamrho_lineEdit.text()) != '':
            string = 'rho='+str(self.RFunctionParamrho_lineEdit.text())
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['survdiff']+'<-survdiff(data='+str(self.RFunctionParam_data)+','+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['survdiff']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
        newData = signals.RSurvFit(data = self.Rvariables['survdiff'])
        self.rSend("survdiff Output", newData)