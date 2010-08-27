"""
<name>RedRplot.mvr</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>pls:plot.mvr</RFunctions>
<tags>PLS</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
class RedRplot_mvr(OWRpy): 
	settingsList = []
	def __init__(self, parent=None, signalManager=None):
		OWRpy.__init__(self)
		self.RFunctionParam_x = ''
		self.inputs.addInput('id0', 'x', redRRModelFit, self.processx)

		
		self.RFunctionParamplottype_comboBox = comboBox(self.controlArea, label = "plottype:", items = ["'prediction'","'validation'","'coefficients'","'scores'","'loadings'","'biplot'","'correlation'"])
		button(self.bottomAreaRight, "Commit", callback = self.commitFunction)
	def processx(self, data):
		if not self.require_librarys(["pls"]):
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
		string = 'plottype='+str(self.RFunctionParamplottype_comboBox.currentText())+''
		injection.append(string)
		inj = ','.join(injection)
		self.Rplot('plot.mvr(x='+str(self.RFunctionParam_x)+','+inj+')')
