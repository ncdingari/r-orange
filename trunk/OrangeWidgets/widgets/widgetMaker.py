"""
<name>Widget Maker</name>
<description>A widget for making the initial framework of a functional widget given an R package and function.</description>
<tags>Special</tags>
<icon>icons/RExecutor.png</icon>
<author>Kyle R. Covington</author>
"""

from OWRpy import *
import redRGUI

class widgetMaker(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        settingsList = ['output_txt', 'parameters']
        OWRpy.__init__(self, parent, signalManager, "File", wantMainArea = 1, resizingEnabled = 1)
        
        self.functionParams = ''
        self.widgetInputsName = []
        self.widgetInputsClass = []
        self.widgetInputsFunction = []
        self.numberInputs = 0
        self.numberOutputs = 0
        
        self.fieldList = {}
        self.functionInputs = {}
        self.processOnConnect = 1
        
        self.inputs = None
        self.outputs = None
        
        # GUI
        # several tabs with different parameters such as loading in a function, setting parameters, setting inputs and outputs
        
        box = redRGUI.widgetBox(self.controlArea, "")
        self.infoa = redRGUI.widgetLabel(box, '')
        self.packageName = redRGUI.lineEdit(box, label = 'Package:', orientation = 1)
        redRGUI.button(box, 'Load Package', callback = self.loadRPackage)
        self.functionName = redRGUI.lineEdit(box, label = 'Function Name:', orientation = 1)
        redRGUI.button(box, 'Parse Function', callback = self.parseFunction)
        self.argsLineEdit = redRGUI.lineEdit(box, label = 'GUI Args')
        self.connect(self.argsLineEdit, SIGNAL('textChanged(QString)'), self.setArgsLineEdit)
        box = redRGUI.widgetBox(self.controlArea, "Inputs and Outputs")
        self.inputArea = QTableWidget()
        box.layout().addWidget(self.inputArea)
        self.inputArea.setColumnCount(4)
        
        #self.inputArea.hide()
        self.connect(self.inputArea, SIGNAL("itemClicked(QTableWidgetItem*)"), self.inputcellClicked)
        redRGUI.button(box, 'Accept Inputs', callback = self.acceptInputs)
        self.functionAllowOutput = redRGUI.checkBox(box, label = None, buttons = ['Allow Output'])
        self.captureROutput = redRGUI.checkBox(box, buttons = ['Show Output'])
        
        redRGUI.button(box, 'Generate Code', callback = self.generateCode)
        redRGUI.button(box, 'Launch Widget', callback = self.launch)
        
        self.splitCanvas = QSplitter(Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)
        
        codebox = redRGUI.widgetBox(self, "Code Box")
        self.splitCanvas.addWidget(codebox)

        self.codeArea = QTextEdit()
        codebox.layout().addWidget(self.codeArea)
        
    def setArgsLineEdit(self, string):
        myargs = str(self.argsLineEdit.text()).split(' ')
        for thisArg in myargs:
            if thisArg not in self.args.keys():
                self.args[thisArg] = ''
                
        self.updateInputs()
    def launch(self):
        import orngEnviron, orngRegistry, orngCanvas
        widgetDirName = os.path.realpath(orngEnviron.directoryNames["widgetDir"])
        #print 'dir:' + widgetDirName
        path = widgetDirName +  "\\widgets\\" + self.functionName.text().replace('.', '_') + ".py"
        #print 'path:' + path
        file = open(os.path.abspath(path), "wt")
        tmpCode = self.completeCode
        tmpCode = tmpCode.replace('<pre>', '')
        tmpCode = tmpCode.replace('</pre>', '')
        tmpCode = tmpCode.replace('&lt;', '<')
        tmpCode = tmpCode.replace('&gt;', '>')
        file.write(tmpCode)
        file.close()
        
        #reload all the widgets including those in the prototype dir we just created 
        #orngCanvas.OrangeCanvasDlg.reloadWidgets()
        
        #orngRegistry.readCategories()
        qApp.canvasDlg.reloadWidgets()  # yay!!! it works
        
        # need to work out how to update the widget icons in the tabs to show the new widget
        #or create a new button that will launch the new widget
        # self.createWidgetsToolbar()
    def loadRPackage(self):
        
        self.require_librarys([str(self.packageName.text())])
        
    def parseFunction(self):
        self.args = {}
        try:
            holder = self.R('capture.output(args('+str(self.functionName.text())+'))')
            s = ''
            functionParams = s.join(holder)
            print str(self.functionName.text())
            self.infoa.setText("Function called successfully.")
            print 'function called successfully'
            print str(self.functionParams)
        except:
            self.infoa.setText("Error with calling function.")
            return
            
        start = functionParams.find('(')+1 #where the args start 
        end = functionParams.rfind(')') # where the args end.
        tmp = functionParams[start:end]
        
        tmp = tmp.replace(' ','') #remove the spaces
        tmp = tmp.replace("','", '##')
        tmp = tmp.replace('","', '##')
        tmp = tmp.split(',')
        for el in tmp:
            tmp2 = el.split('=')
            tmp2[0] = tmp2[0].replace('.', '_')
            if tmp2[0] != '___': # don't pay attention to optional params
                if len(tmp2) > 1:
                    
                    self.args[tmp2[0]] = tmp2[1]
                else:
                    self.args[tmp2[0]] = ''
            
        for arg in self.args.keys():
            if self.args[arg][0:2] == 'c(':
                self.args[arg] = self.args[arg].replace("'", '')
                self.args[arg] = self.args[arg].replace('"', '')
                start = self.args[arg].find('(')+1
                end = self.args[arg].rfind(')')
                self.args[arg] = self.args[arg][start:end] #strip out the brackets
                self.args[arg] = self.args[arg].replace('##', ",")
                self.args[arg] = self.args[arg].split(',')
        
        self.argsLineEdit.setText(' '.join(self.args.keys()))
        self.updateInputs()
        
    def updateInputs(self):
        self.inputArea.clear()
        self.inputArea.setRowCount(int(len(str(self.argsLineEdit.text()).split(' '))))

        self.inputArea.show()
        self.inputArea.setHorizontalHeaderLabels(['Name', 'Class', 'Status', 'Required'])
        n=0
        for arg in str(self.argsLineEdit.text()).split(' '):
            arg = arg.replace('.', '_') # python uses points for class refference
            itemname = QTableWidgetItem(str(arg))
            #itemClass = QTableWidgetItem
            self.inputArea.setItem(n,0,itemname)
            cw = QComboBox()
            cw.addItems(['Widget Input', 'Connection Input'])
            self.inputArea.setCellWidget(n,1,cw)
            ad = QComboBox()
            ad.addItems(['Standard', 'Advanced'])
            self.inputArea.setCellWidget(n,2,ad)
            re = QComboBox()
            re.addItems(['Optional', 'Required'])
            self.inputArea.setCellWidget(n,3,re)
            n += 1
        
    def acceptInputs(self): #accept the criteria in the input Area
        for i in xrange(self.inputArea.rowCount()):
            #print 'i:'+str(i)
            combo = self.inputArea.cellWidget(i, 1)
            #print combo
            if combo.currentText() == 'Widget Input':
                adcombo = self.inputArea.cellWidget(i, 2)
                recombo = self.inputArea.cellWidget(i, 3)

                #print str(self.inputArea.item(i ,0).text())
                self.fieldList[str(self.inputArea.item(i, 0).text())] = ['', adcombo.currentText(), recombo.currentText()]
            else:
                self.functionInputs[str(self.inputArea.item(i,0).text())] = ''
        print self.fieldList
        print self.functionInputs
        for item in self.fieldList.keys():
            item = item.replace('.', '_')
            self.fieldList[item][0] = self.args[item]
            
    def inputcellClicked(self, item):
        self.inputArea.editItem(item)
    
    def generateCode(self):
        self.makeHeader()
        self.makeInitHeader()
        self.makeGUI()
        self.makeProcessSignals()
        self.makeCommitFunction()
        self.makeReportFunction()
        #self.makeRsendFunction()
        
        self.combineCode()
        
    def makeHeader(self):
        self.headerCode = '"""\n'
        self.headerCode += '&lt;name&gt;'+self.functionName.text()+'&lt;/name&gt;\n'
        self.headerCode += '&lt;author&gt;Generated using Widget Maker written by Kyle R. Covington&lt;/author&gt;\n'
        self.headerCode += '"""\n'
        self.headerCode += 'from OWRpy import * \n'
        self.headerCode += 'import redRGUI \n'
        
    def makeInitHeader(self):
        self.initCode = ''
        self.initCode += 'class '+self.functionName.text().replace('.', '_')+'(OWRpy): \n'
        self.initCode += '\tsettingsList = []\n'
        self.initCode += '\tdef __init__(self, parent=None, signalManager=None):\n'

        self.initCode += '\t\tOWRpy.__init__(self, parent, signalManager, "File", wantMainArea = 0, resizingEnabled = 1)\n'
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.initCode += '\t\tself.setRvariableNames(["'+self.functionName.text()+'"])\n'
            self.initCode += '\t\tself.data = {}\n'
        # set's the default's of the fields
        # for element in self.fieldList.keys():
            # if element == '___':
                # pass
            # else:
                # if self.fieldList[element][0] == '' or self.fieldList[element][0] == "":
                    # self.initCode += '\t\tself.RFunctionParam_'+element+' = ""\n'
                # elif type(self.fieldList[element][0]) == type([]): #the fieldList is a list
                    # self.initCode += '\t\tself.RFunctionParam_'+element+' = 0\n' #set the item to the first one
                # else:
                    # self.fieldList[element][0] = self.fieldList[element][0].replace('"', '')
                    # self.fieldList[element][0] = self.fieldList[element][0].replace("'", "")
                    # self.initCode += '\t\tself.RFunctionParam_'+element+' = "'+str(self.fieldList[element][0])+'"\n'
        self.initCode += '\t\tself.loadSettings() \n'
        if len(self.functionInputs.keys()) > 0:
            for inputName in self.functionInputs.keys():
                self.initCode += "\t\tself.RFunctionParam_"+inputName+" = ''\n"
            self.initCode += '\t\tself.inputs = ['
            for element in self.functionInputs.keys():
                self.initCode += '("'+element+'", RvarClasses.RVariable, self.process'+element+'),'
            self.initCode = self.initCode[:len(self.initCode)-1]
            self.initCode += ']\n'
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.initCode += '\t\tself.outputs = [("'+self.functionName.text()+' Output", RvarClasses.RVariable)]\n'
        self.initCode += '\t\t\n'
        
    def makeGUI(self):
        self.guiCode = ''
        self.guiCode += """\t\tself.help.setHtml('<small>Default Help HTML, one should update this as soon as possible.  For more infromation on widget functions and RedR please see either the <a href="http://www.code.google.com/p/r-orange">google code repository</a> or the <a href="http://www.red-r.org">RedR website</a>.</small>')\n"""
        self.guiCode += '\t\tbox = redRGUI.tabWidget(self.controlArea)\n'
        self.guiCode += '\t\tself.standardTab = box.createTabPage(name = "Standard")\n'
        self.guiCode += '\t\tself.advancedTab = box.createTabPage(name = "Advanced")\n'
        for element in self.fieldList.keys():
            if element == '___':
                pass
            else:
                if type(self.fieldList[element][0]) == type(''):
                    if self.fieldList[element][1] == 'Standard':
                        self.guiCode += '\t\tself.RFunctionParam'+ element +'_lineEdit =  redRGUI.lineEdit(self.standardTab,  label = "'+element+':")\n'
                    elif self.fieldList[element][1] == 'Advanced':
                        self.guiCode += '\t\tself.RFunctionParam'+ element +'_lineEdit =  redRGUI.lineEdit(self.advancedTab, label = "'+element+':")\n'
                elif type(self.fieldList[element][0]) == type([]):
                    if self.fieldList[element][1] == 'Standard':
                        self.guiCode += '\t\tself.RFunctionParam' + element +'_comboBox = redRGUI.comboBox(self.standardTab, label = "'+element+':", items = '+str(self.fieldList[element][0])+')\n'
                    elif self.fieldList[element][1] == 'Advanced':
                        self.guiCode += '\t\tself.RFunctionParam' + element +'_comboBox = redRGUI.comboBox(self.advancedTab, label = "'+element+':", items = '+str(self.fieldList[element][0])+')\n'
        self.guiCode += '\t\tredRGUI.button(self.bottomAreaRight, "Commit", callback = self.commitFunction)\n'
        self.guiCode += '\t\tredRGUI.button(self.controlArea, "Report", callback = self.sendReport)\n'
        if 'Show Output' in self.captureROutput.getChecked():
            self.guiCode += '\t\tself.RoutputWindow = redRGUI.textEdit(self.controlArea, label = "RoutputWindow")\n'
            #self.guiCode += '\t\tself.controlArea.layout().addWidget(self.RoutputWindow)\n'

    def makeProcessSignals(self):
        self.processSignals = ''
        for inputName in self.functionInputs.keys():
            self.processSignals += '\tdef process'+inputName+'(self, data):\n'
            if str(self.packageName.text()) != '':
                self.processSignals += '\t\tself.require_librarys(["'+str(self.packageName.text())+'"]) \n'
            self.processSignals += '\t\tif data:\n'
            self.processSignals += '\t\t\tself.RFunctionParam_'+inputName+'=data["data"]\n'
            self.processSignals += '\t\t\tself.data = data.copy()\n'
            if self.processOnConnect:
                self.processSignals += '\t\t\tself.commitFunction()\n'
                
    def makeCommitFunction(self):
        self.commitFunction = ''
        self.commitFunction += '\tdef commitFunction(self):\n'
        for inputName in self.functionInputs.keys():
            self.commitFunction += "\t\tif str(self.RFunctionParam_"+inputName+") == '': return\n"
        for element in self.fieldList.keys():
            if self.fieldList[element][2] == 'Required':
                self.commitFunction += "\t\tif str(self.RFunctionParam"+ element +"_lineEdit.text()) == '': return\n"
        self.commitFunction += "\t\tinjection = []\n"
        for element in self.fieldList.keys():
            self.commitFunction += "\t\tif str(self.RFunctionParam"+ element +"_lineEdit.text()) != '':\n"
            self.commitFunction += "\t\t\tstring = '"+element+"='+str(self.RFunctionParam"+ element +"_lineEdit.text())\n"
            self.commitFunction += "\t\t\tinjection.append(string)\n"
        self.commitFunction += "\t\tinj = ','.join(injection)\n"
        self.commitFunction += "\t\tself.R("
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.commitFunction += "self.Rvariables['"+self.functionName.text()+"']+'&lt;-"+self.functionName.text()+"("
        else:
            self.commitFunction += "'"+self.functionName.text()+"("
        for element in self.functionInputs.keys():
            if element != '___':
                element = element.replace('_', '.')
                self.commitFunction += element+"='+str(self.RFunctionParam_"+element+")+',"
        #self.commitFunction = self.commitFunction[:-2] #remove the last element
        # for element in self.fieldList.keys():
            # if element == '...':
                # pass
            # else:
                # self.commitFunction += element+"='+str(self.RFunctionParam_"+element+")+',"
        # self.commitFunction = self.commitFunction[:-1]
        self.commitFunction += "'+inj+'"
        self.commitFunction += ")')\n"
        if 'Show Output' in self.captureROutput.getChecked():
            self.commitFunction += "\t\tself.R('txt<-capture.output(self.Rvariables['"+self.functionName.text()+"']+')')"
            self.commitFunction += "\t\tself.RoutputWindow.clear()\n"
            self.commitFunction += "\t\ttmp = self.R('paste(txt, collapse =\x22\x5cn\x22)')\n"
            self.commitFunction += "\t\tself.RoutputWindow.insertHtml('&lt;br&gt;&lt;pre&gt;'+tmp+'&lt;/pre&gt;')\n"
            
                    # pasted = self.rsession('paste(txt, collapse = " \n")')
        # self.thistext.insertPlainText('>>>'+self.command+'##Done')
        # self.thistext.insertHtml('<br><pre>'+pasted+'<\pre><br>')
        
        
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.commitFunction += '\t\tself.data["data"] = self.Rvariables["'+self.functionName.text()+'"]\n'
            self.commitFunction += '\t\tself.rSend("'+self.functionName.text()+' Output", self.data)\n'
    def makeReportFunction(self):
        self.reportFunction = ''
        self.reportFunction += '\tdef compileReport(self):\n'
        for inputName in self.functionInputs.keys():
            self.reportFunction += '\t\tself.reportSettings("Input Settings",[("'+inputName+'", self.RFunctionParam_'+inputName+')])\n' # output the inputs of the function
        for element in self.fieldList.keys():
            self.reportFunction += "\t\tself.reportSettings('Function Settings', [('"+element+"',str(self.RFunctionParam"+ element +"_lineEdit.text()"))])\n"
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.reportFunction += '\t\tself.reportRaw(self.Rvariables["'+self.functionName.text()+'"])\n'
            
        self.reportFunction += '\tdef sendReport(self):\n\t\tself.compileReport()\n\t\tself.showReport()\n'

    def combineCode(self):
        self.completeCode = '<pre>'
        self.completeCode += self.headerCode+self.initCode+self.guiCode+self.processSignals+self.commitFunction+self.reportFunction
        self.completeCode += '</pre>'
        self.codeArea.setHtml(self.completeCode)