"""
<name>Fisher Exact Test</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Calculates the Fisher Exact Test.  Takes a matrix of numbers to be used for building the test.</description>
<RFunctions>stats:fisher.test</RFunctions>
<tags>Stats</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals

class RedRfisher_test(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self, parent, signalManager, "fisher_test", wantMainArea = 0, resizingEnabled = 1)
		self.setRvariableNames(["fisher.test"])
		self.data = {}
		self.RFunctionParam_x = ''
		self.inputs = [("x", signals.RMatrix.RMatrix, self.processx)]
		
		self.RFunctionParamB_lineEdit = redRGUI.lineEdit(self.controlArea, label = "Number of Replicates for Monte Carlo:", text = '2000')
		self.RFunctionParamhybrid_checkBox = redRGUI.checkBox(self.controlArea, label = "Hybrid Probabilities:", items = ['FALSE', 'TRUE'], setChecked = 'FALSE')
		self.RFunctionParamsimulate_p_value_lineEdit = redRGUI.checkBox(self.controlArea, label = "simulate_p_value:", items = ['FALSE,TRUE'], setChecked = 'FALSE')
		self.RFunctionParamconf_level_lineEdit = redRGUI.lineEdit(self.controlArea, label = "Confidence Level:", text = '0.95')
		self.RFunctionParamconf_int_lineEdit = redRGUI.checkBox(self.controlArea, label = "Calculate Confidence Interval:", items = ['TRUE','FALSE'], setChecked = 'TRUE')
		self.RFunctionParamalternative_comboBox = redRGUI.comboBox(self.controlArea, label = "Alternative Hypothesis:", items = ["two.sided","greater","less"])
		self.RFunctionParamor_lineEdit = redRGUI.lineEdit(self.controlArea, label = "Odds Ratio:", text = '1')
		redRGUI.button(self.bottomAreaRight, "Commit", callback = self.commitFunction)
		self.RoutputWindow = redRGUI.textEdit(self.controlArea, label = "R Output Window")
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
		if str(self.RFunctionParam_x) == '': return
		injection = []
		if str(self.RFunctionParamcontrol_lineEdit.text()) != '':
			string = 'control='+str(self.RFunctionParamcontrol_lineEdit.text())+''
			injection.append(string)
		if str(self.RFunctionParamB_lineEdit.text()) != '':
			string = 'B='+str(self.RFunctionParamB_lineEdit.text())+''
			injection.append(string)
		injection.append('hybrid ='+ str(self.RFunctionParamhybrid_checkBox.getChecked()))
		injection.append('simulate.p.value='+str(self.RFunctionParamsimulate_p_value_lineEdit.getChecked()))
		if str(self.RFunctionParamconf_level_lineEdit.text()) != '':
			string = 'conf.level='+str(self.RFunctionParamconf_level_lineEdit.text())+''
			injection.append(string)
		injection.append('conf.int='+str(self.RFunctionParamconf_int_lineEdit.text()))
		string = 'alternative='+str(self.RFunctionParamalternative_comboBox.currentText())+''
		injection.append(string)
		if str(self.RFunctionParamor_lineEdit.text()) != '':
			string = 'or='+str(self.RFunctionParamor_lineEdit.text())+''
			injection.append(string)
		inj = ','.join(injection)
		self.R(self.Rvariables['fisher.test']+'<-fisher.test(x='+str(self.RFunctionParam_x)+','+inj+')')
		self.R('txt<-capture.output('+self.Rvariables['fisher.test']+')')
		self.RoutputWindow.clear()
		tmp = self.R('paste(txt, collapse ="\n")')
		self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
