"""
<name>Contour Plot</name>
<tags>Plotting</tags>
<icon>plot.png</icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals
import libraries.plotting.signalClasses as plotSignals
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.signalClasses.RList import RList as redRList
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRDataFrame


from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
#from libraries.base.qtWidgets.graphicsView import graphicsView
from libraries.plotting.qtWidgets.redRGGPlot import redRGGPlot
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.spinBox import spinBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class krcggplotcontour(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        self.require_librarys(["ggplot2", "hexbin"])
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.setRvariableNames(["contour"])
        #self.dataFrame = ''
        #self.plotAttributes = {}
        #self.RFunctionParam_plotatt = ''
        self.inputs.addInput('id0', 'Data Table', redRDataFrame, self.processy)
        #self.inputs.addInput('id1', 'x', redRRVector, self.processx)
        #self.inputs.addInput('id2', 'plotatt', redRRPlotAttribute, self.processplotatt, multiple = True)

        
        self.RFunctionParamxlab_lineEdit = lineEdit(self.controlArea, label = "X Label:", text = 'X Label')
        self.RFunctionParamylab_lineEdit = lineEdit(self.controlArea, label = "Y Label:", text = 'Y Label')
        self.RFunctionParammain_lineEdit = lineEdit(self.controlArea, label = "Main Title:", text = 'Main Title')
        self.namesListX = comboBox(self.controlArea, label = 'X Axis Data:')
        #self.namesListX.setEnabled(False)
        self.namesListY = comboBox(self.controlArea, label = 'Y Axis Data:')
        #self.namesListY.setEnabled(False)
        self.namesListZ = comboBox(self.controlArea, label = 'Z Contours:')
        self.binwidth = spinBox(self.controlArea, label = 'Binsizes:', min = 0, value = 5)
        self.graphicsView = redRGGPlot(self.controlArea,label='Contour Plot',displayLabel=False,
        name = self.captionTitle)
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        
    def processy(self, data):
        
        if data:
            self.RFunctionParam_y = data.getData()
            self.namesListX.setEnabled(True)
            self.namesListX.update(self.R('names('+data.getData()+')'))
            self.namesListY.setEnabled(True)
            self.namesListY.update(self.R('names('+data.getData()+')'))
            self.namesListZ.setEnabled(True)
            self.namesListZ.update(self.R('names('+data.getData()+')'))
            self.dataFrame = data.getData()
            self.dataFrameAttached = True

            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.graphicsView.clear()
            self.RFunctionParam_y=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if self.namesListY.currentText() == self.namesListX.currentText(): 
            self.status.setText(_("X and Y data can't be the same"))
            return
        injection = []
        if unicode(self.RFunctionParamxlab_lineEdit.text()) != '':
            string = 'xlab=\''+unicode(self.RFunctionParamxlab_lineEdit.text())+'\''
            injection.append(string)
        if unicode(self.RFunctionParamylab_lineEdit.text()) != '':
            string = 'ylab=\''+unicode(self.RFunctionParamylab_lineEdit.text())+'\''
            injection.append(string)
        if unicode(self.RFunctionParammain_lineEdit.text()) != '':
            string = 'main=\''+unicode(self.RFunctionParammain_lineEdit.text())+'\''
            injection.append(string)
        inj = ','.join(injection)
        self.R('%(VAR)s<-ggplot(%(DATA)s, aes(x = %(XDATA)s, y = %(YDATA)s, z = %(ZDATA)s))' % {'DATA':self.RFunctionParam_y, 'VAR':self.Rvariables['contour'], 'XDATA':self.namesListX.currentText(), 'YDATA':self.namesListY.currentText(), 'ZDATA':self.namesListZ.currentText()}, wantType = 'NoConversion')
        self.R('%(VAR)s <- %(VAR)s + stat_contour(binwidth = %(BIN)s)' % {'VAR':self.Rvariables['contour'], 'BIN':self.binwidth.value()}, wantType = 'NoConversion')
        self.graphicsView.plot(query = self.Rvariables['contour'], function = '')
    
    