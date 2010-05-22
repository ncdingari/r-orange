"""
<name>Normalize</name>
<description>Processes an Affybatch to an eset using RMA</description>
<tags>Microarray</tags>
<RFunctions>affy:rma,affy:mas5,affy:expresso</RFunctions>
<icon>icons/normalize.png</icon>
<priority>1010</priority>
"""


from OWRpy import *
# import OWGUI
import signals
import redRGUI 


class affyNormalize(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, parent, 'Affy Normalize', signalManager, "Normalization")
        
        self.normmeth = 'quantiles'
        self.normoptions = ''
        self.norm = ['quantiles']
        self.data = ''
        self.enableMethBox = False
        self.norminfo = ''
        
        self.saveSettingsList.append(['norm', 'normmeth', 'normoptions', 'data', 'enableMethBox', 'norminfo'])
        
        self.require_librarys(['affy'])
        
        
        
        #set R variable names
        self.setRvariableNames(['normalized_Eset'])
        
        #signals
        self.inputs = [("AffyBatch", signals.affy.RAffyBatch, self.process)]
        self.outputs = [("Normalized Eset", signals.affy.REset)]

        
        #the GUI
        self.selMethBox = redRGUI.radioButtons(self.controlArea, label='Normalization Method',
        buttons=["RMA", "MAS5", "Custom"], 
        callback=self.selectMethodChanged,orientation='horizontal')
        self.selMethBox.setChecked('RMA')
        
        info = redRGUI.groupBox(self.controlArea, label = "Normalization Options")

        
        #insert a block to check what type of object is connected.  If nothing connected set the items of the normalize methods objects to 
        self.normselector = redRGUI.comboBox(info, label="Normalization Method", items=self.norm, orientation=0)
        self.normselector.setEnabled(False)
        self.bgcorrectselector = redRGUI.comboBox(info, label="Background Correct Methods", items=['TRUE', 'FALSE'], orientation=0)
        self.bgcorrectselector.setEnabled(False)
        self.bgcmethselector = redRGUI.comboBox(info, label="Background Correct Methods", items=[],
        #self.R('bgcorrect.methods'), 
        orientation=0)
        self.bgcmethselector.setEnabled(False)
        self.pmcorrectselector = redRGUI.comboBox(info, label="Perfect Match Correct Methods",
        items=[]
        #self.R('pmcorrect.methods')
        , orientation=0)
        self.pmcorrectselector.setEnabled(False)
        self.summethselector = redRGUI.comboBox(info, label="Summary Methods", items=[]
        #self.R('express.summary.stat.methods')
        , orientation=0)
        self.summethselector.setEnabled(False)
        
        
        runbutton = redRGUI.button(self.bottomAreaRight, label = "Run Normalization", callback = self.normalize)
        # runbutton.layout().setAlignment(Qt.AlignRight)
        
        self.resize(400, 200)
    def normalize(self):
        if self.data == '': return
        self.status.setText('Processing')
        if self.selMethBox.getChecked() == 'RMA':
            self.R(self.Rvariables['normalized_Eset']+'<-rma('+self.data+')',True) #makes the rma normalization
            self.norminfo = 'Normalized with RMA'
        if self.selMethBox.getChecked() == 'MAS5':
            self.R(self.Rvariables['normalized_Eset']+'<-mas5('+self.data+')',True) #makes the mas5 normalization
            self.norminfo = 'Normalized with MAS5'
        if self.selMethBox.getChecked() == 'Custom':
            self.R(self.Rvariables['normalized_Eset']+'<-expresso('+self.data+', bg.correct='+self.bgcorrectselector.currentText()+', bgcorrect.method="'+self.bgcmethselector.currentText()+'", pmcorrect.method="'+self.pmcorrectselector.currentText()+'", summary.method="'+self.summethselector.currentText()+'")',True)
            self.norminfo = 'Normalized by: Background Correction:'+self.bgcorrectselector.currentText()+', Method:'+self.bgcmethselector.currentText()+', Perfect Match Correct Method: '+self.pmcorrectselector.currentText()+', Summary Method: '+self.summethselector.currentText()
        self.toSend()
        self.status.setText(self.norminfo)
        
    # def collectOptions(self):
        # if self.normselector.currentText() == None: self.normoptions = ""
        # elif self.normselector.currentText() == "":
            ##self.normselector.setText("")
            # self.collectOptions()
        # else:
            # self.normoptions = ',method='+self.normselector.currentText()
    
    def process(self, dataset):
        #required librarys

        # self.rSend("Normalized Expression Matrix", None) #start the killing cascade because normalization is required
        # self.rSend("Normalized Eset", None) #start the killing cascade because normalization is required
                
        try: 
            # print str(dataset['data'])
            # print dataset.__class__
            print dataset
            self.data = str(dataset.getData())
            
            if self.R('length(exprs('+self.data+')[1,])') > 10:
                self.selectMethod = 2
                self.selectMethodChanged()
                
            else:
                self.selectMethod = 0
                self.selectMethodChanged()
                
            self.selMethBox.setEnabled(True)
            self.status.setText('Data Loaded')
        except: 
            print '|###| error'

        
        self.bgcmethselector.update(self.R('bgcorrect.methods()'))
        self.pmcorrectselector.update(self.R('pmcorrect.methods()'))
        self.summethselector.update(self.R('express.summary.stat.methods()'))
        
    
    def selectMethodChanged(self):

        if self.selMethBox.getChecked() == 'RMA':
            self.bgcorrectselector.setEnabled(False)
            self.bgcmethselector.setEnabled(False)
            self.pmcorrectselector.setEnabled(False)
            self.summethselector.setEnabled(False)
            self.normselector.setEnabled(False)
        elif self.selMethBox.getChecked() == 'MAS5':
            self.bgcorrectselector.setEnabled(False)
            self.bgcmethselector.setEnabled(False)
            self.pmcorrectselector.setEnabled(False)
            self.summethselector.setEnabled(False)
            self.normselector.setEnabled(False)
        elif self.selMethBox.getChecked() == 'Custom':
            self.bgcorrectselector.setCurrentIndex(self.bgcorrectselector.findText('FALSE'))
            self.bgcorrectselector.setEnabled(True)
            self.bgcorrectmeth = 'none'
            self.bgcmethselector.setCurrentIndex(self.bgcmethselector.findText('none'))
            self.bgcmethselector.setEnabled(True)
            self.pmcorrect = 'pmonly'
            self.pmcorrectselector.setCurrentIndex(self.pmcorrectselector.findText('pmonly'))
            self.pmcorrectselector.setEnabled(True)
            self.summarymeth = 'liwong'
            self.summethselector.setCurrentIndex(self.summethselector.findText('liwong'))
            self.summethselector.setEnabled(True)
            self.norm = ['quantiles']
            self.normselector.clear()
            if self.data != '': # normalize.methods() results in an error in R
                self.normselector.addItems(self.R('normalize.methods('+self.data+')'))
                self.normselector.setCurrentIndex(self.normselector.findText('invariantset'))
                self.normselector.setEnabled(True)

    def toSend(self):
        signals.setGlobalData(self,'eset',self.Rvariables['normalized_Eset'],description='Normalized Eset')
        
        newData = signals.affy.REset(data = self.Rvariables['normalized_Eset'])
        self.rSend("Normalized Eset", newData)
        
    