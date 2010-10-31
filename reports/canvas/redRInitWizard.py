from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox
from libraries.base.qtWidgets.groupBox import groupBox as redRgroupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit
from libraries.base.qtWidgets.listBox import listBox as redRlistBox
from libraries.base.qtWidgets.button import button as redRButton
## redR-IntroWizard.  a wizard that is shown on first load that guides the user through the setup of Red-R.  The user will be encouraged to register Red-R (e-mail address), set canvas options (error reporting, output level, showing the output on error), R options (R mirror)

import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRGUI
import RSession, redREnviron

class RedRInitWizard(QWizard):
    def __init__(self, parent = None):
        QWizard.__init__(self, parent)
        self.libs = {}
        #layout = [QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton]
        #self.setButtonLayout(layout)
        self.setWindowTitle('Red-R Setup')
        self.settings = dict(redREnviron.settings)
        self.registerPage = QWizardPage()
        self.registerPage.setLayout(QVBoxLayout())
        self.registerPage.setTitle('Please Register Red-R')
        self.registerPage.setSubTitle('Registration will help us track errors to make Red-R better.')
        
        self.email = redRlineEdit(self.registerPage, label = 'Email Address (Optional):', width = -1)
        self.allowContact = redRradioButtons(self.registerPage, label = 'Red-R can contact me to ask about errors:', buttons = ['Yes', 'No'])
        self.allowContact.setChecked('Yes')
        
        self.errorReportingPage = QWizardPage()
        self.errorReportingPage.setLayout(QVBoxLayout())
        self.errorReportingPage.setTitle('Error Reporting')
        self.errorReportingPage.setSubTitle('How would you like errors to be reported to Red-R.')
        self.redRExceptionHandling = redRcheckBox(self.errorReportingPage, buttons = ['Show output window on exception', 'Print last exception in status bar', 'Submit Error Report', 'Always ask before submitting error report'], toolTips = ['Check this if you want to see the output when an error happens.', 'Check this if you want the last exception printed in the status bar.', 'Check this if you want to send errors to Red-R.\nWe will only show the errors to Red-R or package maintainers.', 'Check this if you want to be asked before a report is sent to Red-R.\nOtherwise a report will be sent automatically to Red-R.'])
        self.redRExceptionHandling.setChecked(['Submit Error Report'])
        
        
        self.RSetupPage = QWizardPage()
        self.RSetupPage.setLayout(QVBoxLayout())
        self.RSetupPage.setTitle('R Repository')
        self.RSetupPage.setSubTitle('Please set the repository closest to you.  This will help you get R packages faster.')
        self.rlibrariesBox = redRgroupBox(self.RSetupPage, 'R Libraries')
        self.libInfo = redRwidgetLabel(self.rlibrariesBox, label='Repository URL: '+ self.settings['CRANrepos'])
        

        # place a listBox in the widget and fill it with a list of mirrors
        redRButton(self.rlibrariesBox, 'Get Libraries', callback = self.loadMirrors)
        self.libListBox = redRlistBox(self.rlibrariesBox, label = 'Mirrors', callback = self.setMirror)
        self.libMessageBox = redRwidgetLabel(self.rlibrariesBox)
        
        self.runExamplePage = QWizardPage()
        self.runExamplePage.setLayout(QVBoxLayout())
        self.runExamplePage.setTitle('Finish')
        self.runExamplePage.setSubTitle('Thanks for setting up Red-R.\n\nIf you want to start an example schema to help you get started then check the "Start Example" box.')
        self.showExample = redRcheckBox(self.runExamplePage, buttons = ['Start Example'], setChecked=['Start Example'])
        
        
        self.addPage(self.registerPage)
        self.addPage(self.errorReportingPage)
        self.addPage(self.RSetupPage)
        self.addPage(self.runExamplePage)
    def loadMirrors(self):
        self.libMessageBox.clear()
        if not redREnviron.checkInternetConnection():
            self.libMessageBox.setText('No Internet Connection, please try again')
            return
        self.libs = RSession.Rcommand('getCRANmirrors()')
        self.libListBox.update(self.libs['Name'])
    def setMirror(self):
        if len(self.libs) == 0: return
        item = self.libListBox.currentRow()
        self.settings['CRANrepos'] = str(self.libs['URL'][item])
        RSession.Rcommand('local({r <- getOption("repos"); r["CRAN"] <- "' + str(self.libs['URL'][item]) + '"; options(repos=r)})')
        #print self.settings['CRANrepos']
        self.libInfo.setText('Repository URL changed to: '+str(self.libs['URL'][item]))