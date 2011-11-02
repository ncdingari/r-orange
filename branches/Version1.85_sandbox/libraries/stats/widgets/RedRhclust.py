"""
<name>Hierarchical Clustering</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Performs a variety of clustering functions on a matrix of data.  Data can be connected in the RDataFrame form but should contain only numeric data.  If not then an error may be reported or the widget may not function as anticipated.  Please see the R help for the function hclust or a statistics text on clustering for more information on different clustering methods.</description>
<RFunctions>stats:hclust</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI, signals
import redRGUI 

class RedRhclust(OWRpy): 
    settingsList = []
    def __init__(self, **kwargs):
        OWRpy.__init__(self, **kwargs)
        self.setRvariableNames(["hclust"])
        self.data = {}
        self.RFunctionParam_d = ''
        self.inputs.addInput('id0', 'd', signals.base.RDataFrame, self.processd)

        self.outputs.addOutput('id0', 'hclust Output', signals.base.RList)

        
        self.RFunctionParammethod_comboBox = redRGUI.base.comboBox(self.controlArea, label = "Cluster Method:", items = ["complete","ward","single","average","mcquitty","centroid"])
        self.RFunctionParamdistmethod_comboBox = redRGUI.base.comboBox(self.controlArea, label = 'Dist Method:', items = ["euclidean", "maximum", "manhattan", "canberra", "binary", "minkowski"])
        redRGUI.base.commitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processd(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_d=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_d=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_d) == '': 
            self.status.setText('No data to process')
            return
        injection = []
        string = 'method=\''+unicode(self.RFunctionParammethod_comboBox.currentText())+'\''
        injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['hclust']+'<-hclust(d=dist(x='+unicode(self.RFunctionParam_d)+', method = \''+unicode(self.RFunctionParamdistmethod_comboBox.currentText())+'\'),'+inj+')')
        newData = signals.base.RList(self, data = self.Rvariables["hclust"], checkVal = False) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)