"""
<name>Generic Plot</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Generic plot is the basis of most RedR plotting.  This accepts fits, data tables, or other RedR outputs and attempts to plot them.  However, there is no guarantee that your data will plot correctly.</description>
<tags>Plotting</tags>
<icon>icons/plot.PNG</icon>

"""
from OWRpy import * 
import OWGUI 
import RRGUI
class plot(OWRpy): 
    settingsList = ['RFunctionParam_cex', 'RFunctionParam_main', 'RFunctionParam_xlab', 'RFunctionParam_ylab']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, signalManager, "File", wantMainArea = 0, resizingEnabled = 1)
        self.RFunctionParam_main = ''
        self.RFunctionParam_xlab = ''
        self.RFunctionParam_ylab = ''
        self.RFunctionParam_cex = '100'
        self.data = {}
        #self.RFunctionParam_y = ''
        self.loadSettings()
        self.RFunctionParam_x = ''
        self.inputs = [("x", RvarClasses.RVariable, self.processx)]
        
        box = OWGUI.widgetBox(self.controlArea, "Widget Box")
        RRGUI.lineEdit(box, None, self, 'RFunctionParam_main', label = 'Main Title:')
        RRGUI.lineEdit(box, None, self, 'RFunctionParam_xlab', label = 'X Axis Label:')
        RRGUI.lineEdit(box, None, self, 'RFunctionParam_ylab', label = 'Y Axis Label:')
        RRGUI.lineEdit(box, None, self, 'RFunctionParam_cex', label = 'Text Magnification Percent:')
        OWGUI.button(box, self, "Commit", callback = self.commitFunction)
    def processx(self, data):
        if data:
            self.data = data
            self.RFunctionParam_x=data["data"]
            self.commitFunction()
    def commitFunction(self):
        #if self.RFunctionParam_y == '': return
        if self.RFunctionParam_x == '': return
        injection = []
        if self.R('class('+str(self.RFunctionParam_x)+')') == 'data.frame' and not 'colors' in self.data:
            injection.append('pch=rownames('+self.RFunctionParam_x+')')
        if self.RFunctionParam_main != '':
            injection.append('main = "'+self.RFunctionParam_main+'"')
        if self.RFunctionParam_xlab != '':
            injection.append('xlab = "'+self.RFunctionParam_xlab+'"')
        if self.RFunctionParam_ylab != '':
            injection.append('ylab = "'+self.RFunctionParam_ylab+'"')
        if self.RFunctionParam_cex != '100':
            mag = float(self.RFunctionParam_cex)/100
            injection.append('cex.lab = '+str(mag))
            injection.append('cex.axis = '+str(mag))
        if injection != []:
            inj = ','+','.join(injection)
        else: inj = ''
        #try:
        self.Rplot('plot('+str(self.RFunctionParam_x)+inj+')')
        # except:
            # QMessageBox.information(None, 'Plotting Error', 'Your plot failed, this may not be a supported plot type.', QMessageBox.Ok)
