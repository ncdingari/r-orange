"""
:Name: Read File
:Icon: readfile.png
:Authors: Red-R Development Team
:Summary: Read data files into Red-R.
:Details: This widget will read data from tab, comma, or space delimited text files. On Microsoft Windows it will also ready Excel files. Click the browse button to search your computer for the file to read. Select how the columns are delimited. On data read or change in these options, the first few lines of the file will be scanned. R will try to automaticlly determine the type of the column. The column data types can be changed. Once the data, column and row header information is properly selected click Load Data to read the full file into Red-R and send forward.
:Outputs: `signals.base.RDataFrame`
"""

from OWRpy import *
import redRGUI, signals
import redRGUI, signals
import re
import textwrap
import cPickle
import pickle
import types
import redRReports

import libraries.base.signalClasses.RDataFrame as rdf


import redRi18n
_ = redRi18n.get_(package = 'base')
class readFile(OWRpy):
    """
        asdfasdfsd
        
        :py:class:`signals.base.RDataFrame`
    """
    globalSettingsList = ['filecombo','path']
    def __init__(self, **kwargs):
        """asdfasdfasdaaaaaaaaaaaaaaaaaaaaaaaaaa"""
        OWRpy.__init__(self, **kwargs)
        self.path = os.path.abspath('/')
        self.colClasses = []
        self.myColClasses = []
        self.colNames = []
        self.dataTypes = []
        self.useheader = 1
        """.. rrvnames::""" ## left blank so no description        
        self.setRvariableNames(['dataframe_org','dataframe_final','filename', 'parent'])
        
        
        """.. signals::"""  ## left blank so no description
        self.outputs.addOutput('od1', _('Output Data'), signals.base.RDataFrame)
        
        #GUI
        area = redRGUI.base.widgetBox(self.controlArea,orientation='horizontal',alignment=Qt.AlignTop)       
        #area.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding ,QSizePolicy.MinimumExpanding))
        #area.layout().setAlignment(Qt.AlignTop)
        options = redRGUI.base.widgetBox(area,orientation='vertical')
        options.setMaximumWidth(300)
        # options.setMinimumWidth(300)
        options.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #area.layout().setAlignment(options,Qt.AlignTop)
        
        
        self.browseBox = redRGUI.base.groupBox(options, label=_("Load File"), 
        addSpace = True, orientation='vertical')
        box = redRGUI.base.widgetBox(self.browseBox,orientation='horizontal')
        """.. rrgui::
            :class: base.fileNamesComboBox
            :label: Files
            :description: Sets the file that the widget is reading and immediatly scans the file.
        """
        self.filecombo = redRGUI.base.fileNamesComboBox(box, label=_('Files'), displayLabel=False,
        orientation='horizontal', callback=self.scanNewFile)
        #self.filecombo.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        
        """,, rrgui::
            :class: base.button
            :label: Browse
            :description: Opens a file browser to search for files.
        """
        redRGUI.base.button(box, label = _('Browse'), callback = self.browseFile)
        
        """.. rrgui::""" # this rrgui call is blank so the parser has to get the info from the .py file directly...
        self.fileType = redRGUI.base.radioButtons(options, label=_('File Type'),
        buttons = [_('Text'), _('Excel'), _('Clipboard')], setChecked=_('Text'),callback=self.scanNewFile,
        orientation='horizontal')
        #self.fileType.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        self.fileType.hide()

        """.. rrgui::"""
        self.delimiter = redRGUI.base.radioButtons(options, label=_('Column Seperator'),
        buttons = [_('Tab'), _('Comma'), _('Space'),_('Other')], setChecked=_('Tab'),callback=self.scanNewFile,
        orientation='horizontal')
        
        """.. rrgui::"""
        self.otherSepText = redRGUI.base.lineEdit(self.delimiter.box,label=_('Seperator'), displayLabel=False,
        text=';',width=20,orientation='horizontal')
        QObject.connect(self.otherSepText, SIGNAL('textChanged(const QString &)'), self.otherSep)
        
        """.. rrgui::"""
        self.headersBox = redRGUI.base.groupBox(options, label=_("Row and Column Names"), 
        addSpace = True, orientation ='horizontal')
        
        """.. rrgui::"""
        self.hasHeader = redRGUI.base.checkBox(self.headersBox,label=_('Column Header'), displayLabel=False, 
        buttons = [_('Column Headers')],setChecked=[_('Column Headers')],
        toolTips=[_('a logical value indicating whether the file contains the names of the variables as its first line. If missing, the value is determined from the file format: header is set to TRUE if and only if the first row contains one fewer field than the number of columns.')],
        orientation='vertical',callback=self.scanNewFile)
        
        """.. rrgui::"""
        self.rowNamesCombo = redRGUI.base.comboBox(self.headersBox,label=_('Select Row Names'), 
        orientation='vertical',callback=self.scanFile)
        #self.rowNamesCombo.setMaximumWidth(250)        
        
        self.otherOptionsBox = redRGUI.base.groupBox(options, label=_("Other Options"), 
        addSpace = True, orientation ='vertical')
        # box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        split = redRGUI.base.widgetBox(self.otherOptionsBox,orientation='horizontal')
        # split.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        """.. rrgui::"""
        self.otherOptions = redRGUI.base.checkBox(split,label=_('Options'), displayLabel=False,
        buttons=['fill','strip.white','blank.lines.skip',
        'allowEscapes','StringsAsFactors'],
        setChecked = ['blank.lines.skip'],
        toolTips = [_('logical. If TRUE then in case the rows have unequal length, blank fields are implicitly added.'),
        _('logical. Used only when sep has been specified, and allows the unicodeipping of leading and trailing white space from character fields (numeric fields are always unicodeipped). '),
        _('logical: if TRUE blank lines in the input are ignored.'),
        _('logical. Should C-style escapes such as \n be processed or read verbatim (the default)? '),
        _('logical: should character vectors be converted to factors?')],
        orientation='vertical',callback=self.scanFile)
        # box.layout().addWidget(self.otherOptions,1,1)
        box2 = redRGUI.base.widgetBox(split,orientation='vertical')
        #box2.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        split.layout().setAlignment(box2,Qt.AlignTop)
        
        """.. rrgui::"""
        self.quote = redRGUI.base.lineEdit(box2,text='"',label=_('Quote:'), width=50, orientation='horizontal')
        
        """.. rrgui::"""
        self.decimal = redRGUI.base.lineEdit(box2, text = '.', label = _('Decimal:'), width = 50, orientation = 'horizontal', toolTip = _('Decimal sign, some countries may want to use the \'.\''))
        
        """.. rrgui::"""
        self.numLinesScan = redRGUI.base.lineEdit(box2,text='10',label=_('# Lines to Preview:'), 
        toolTip=_('The maximum number of rows to read in while previewing the file. Negative values are ignored.'), 
        width=50,orientation='horizontal')
        
        """.. rrgui::"""
        self.numLinesReads = redRGUI.base.lineEdit(box2,text='-1',label=_('# Lines to Read:'), 
        toolTip=_('Number of lines to read from file. Read whole file if 0 or negative values.'), 
        width=50,orientation='horizontal')

        """.. rrgui::"""
        self.numLinesSkip = redRGUI.base.lineEdit(box2,text='0',label=_('# Lines to Skip:'),
        toolTip=_("The number of lines of the data file to skip before beginning to read data."), 
        width=50,orientation='horizontal')
        
        holder = redRGUI.base.widgetBox(options,orientation='horizontal')
        #clipboard = redRGUI.base.button(holder, label = _('Load Clipboard'), 
        # toolTip = _('Load the file from the clipboard, you can do this if\ndata has been put in the clipboard using the copy command.'), 
        # callback = self.loadClipboard)
        """.. rrgui::"""
        rescan = redRGUI.base.button(holder, label = _('Rescan File'),toolTip=_("Preview a small portion of the file"),
        callback = self.scanNewFile)
        """.. rrgui::"""
        load = redRGUI.base.button(holder, label = _('Load File'),toolTip=_("Load the file into Red-R"),
        callback = self.loadFile)
        holder.layout().setAlignment(Qt.AlignRight)

        """.. rrgui::"""
        self.FileInfoBox = redRGUI.base.groupBox(options, label = _("File Info"), addSpace = True)       
        self.infob = redRGUI.base.widgetLabel(self.FileInfoBox, label='',wordWrap=True)
        self.infoc = redRGUI.base.widgetLabel(self.FileInfoBox, label='')
        self.FileInfoBox.setHidden(True)
        
        
        """.. rrgui::"""
        self.tableArea = redRGUI.base.widgetBox(area)
        self.tableArea.setMinimumWidth(500)
        #self.tableArea.setHidden(True)
        self.tableArea.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        """.. rrgui::"""
        self.scanarea = redRGUI.base.textEdit(self.tableArea,label= _('File Preview'),includeInReports=False)
        self.scanarea.setLineWrapMode(QTextEdit.NoWrap)
        self.scanarea.setReadOnly(True)
        self.scroll = redRGUI.base.scrollArea(self.tableArea);
        
        self.columnTypes = redRGUI.base.widgetBox(self,orientation=QGridLayout(),margin=10);
        self.scroll.setWidget(self.columnTypes)
        self.columnTypes.layout().setSizeConstraint(QLayout.SetMinAndMaxSize)
        #self.setFileList()
        import sys
        if sys.platform=="win32":
            self.require_librarys(['RODBC'])
            self.setForExcel()

    def setForExcel(self):
        self.fileType.show()
    def otherSep(self,text):
        self.delimiter.setChecked('other')
        
    def loadCustomSettings(self,settings):
        if not self.filecombo.getCurrentFile():
            redRGUI.base.widgetLabel(self.browseBox,label=_('The loaded file is not found on your computer.\nBut the data saved in the Red-R session is still available.')) 
        for i in range(len(self.colClasses)):
            s = redRGUI.base.radioButtons(self.columnTypes,label=self.colNames[i],displayLabel=False,
            buttons = ['factor','numeric','character','integer','logical'], 
            orientation = 'horizontal', callback = self.updateColClasses)
            
            s.setChecked(self.myColClasses[i])
            if not self.filecombo.getCurrentFile():
                s.setEnabled(False)
            q = redRGUI.base.widgetLabel(self.columnTypes,label=self.colNames[i])
            self.columnTypes.layout().addWidget(s.controlArea, i, 1)
            self.columnTypes.layout().addWidget(q.controlArea, i, 0)
            
    
    def browseFile(self): 
        print self.path
        fn = QFileDialog.getOpenFileName(self, _("Open File"), self.path,
        "Text file (*.txt *.csv *.tab *.xls);; All Files (*.*)")
        #print unicode(fn)
        if fn.isEmpty(): return
        fn = unicode(fn)
        # print type(fn), fn
        
        self.path = os.path.split(fn)[0]
        self.filecombo.addFile(fn)
        self.saveGlobalSettings()
        self.scanNewFile()

    def scanNewFile(self):
        self.removeInformation()
        self.removeWarning()
        
        if self.fileType.getChecked() == _('Excel'):
            self.delimiter.setDisabled(True)
            self.otherOptionsBox.setDisabled(True)
            self.headersBox.setDisabled(True)
            self.columnTypes.setDisabled(True)
        else:
            self.delimiter.setEnabled(True)
            self.otherOptionsBox.setEnabled(True)
            self.headersBox.setEnabled(True)
            self.columnTypes.setEnabled(True)
        
        for i in self.columnTypes.findChildren(QWidget):
            i.setHidden(True)
          
        self.rowNamesCombo.clear()
        self.colClasses = []
        self.colNames = []
        self.dataTypes = []
        
        self.loadFile(scan=True)
    
    def updateColClasses(self):
        self.myColClasses = []
        for i in self.dataTypes:
            self.myColClasses.append(unicode(i[1].getCheckedId()))
        self.loadFile(scan=True)
    def scanFile(self):
        self.loadFile(scan=True)

    # def loadClipboard(self):
        # self.loadFile(scan = 'clipboard')
    
    def loadFile(self,scan=False):
        #print scan

        fn = self.filecombo.getCurrentFile()
        if not fn and not scan == 'clipboard':
            print _('No file selected')
            return 
        if not self.fileType.getChecked() ==_('Clipboard'):
            self.R('%s <- "%s"' % (self.Rvariables['filename'] , fn)) 
            

            if self.delimiter.getCheckedId() =='Tab':
                sep  = '\t'
            elif self.delimiter.getCheckedId() =='Comma':
                sep  = ','
            elif self.delimiter.getCheckedId() =='Space':
                sep  = ' '
            elif self.delimiter.getCheckedId() == 'Other':
                sep = unicode(self.otherSepText.text())
            else:
                sep = self.delimiter.getChecked()
            otherOptions = ''
            for i in self.otherOptions.getCheckedIds():
                otherOptions += unicode(i) + '=TRUE,' 
        else:
            sep = ''
            otherOptions = ''
            for i in self.otherOptions.getCheckedIds():
                otherOptions += unicode(i) + '=TRUE,'
        if 'Column Headers' in self.hasHeader.getChecked():
            header = 'TRUE'
        else:
            header = 'FALSE'
        
        
        if scan:
            nrows = unicode(self.numLinesScan.text())
            processing=False
        else:
            if int(self.numLinesReads.text()) > 0:
                nrows = unicode(self.numLinesReads.text())
            else:
                nrows = '-1'
            processing=True
        
        
        
        if self.rowNamesCombo.currentIndex() not in [0,-1]:
            self.rownames = self.rowNamesCombo.currentText()
            param_name = '"' + self.rownames + '"'
        else:
            param_name = 'NULL' 
            self.rownames = 'NULL'
        
        cls = []
        for i,new,old in zip(xrange(len(self.myColClasses)),self.myColClasses,self.colClasses):
            if new != old:
                cls.append(self.dataTypes[i][0] + '="' + new + '"')
        
        if len(cls) > 0:
            ccl = 'c(' + ','.join(cls) + ')'
        else:
            ccl = 'NA'
        Runicode = 'None'
        try:
            if self.fileType.getChecked() == _('Excel'):
                
                self.R('channel <- odbcConnectExcel(%s)' %(self.Rvariables['filename']))
                table = self.R('sqlTables(channel)$TABLE_NAME[1]')
                if not scan:
                    nrows = '0'
                RStr = '%s <- sqlQuery(channel, "select * from [%s]",max=%s)' % (self.Rvariables['dataframe_org'], table,nrows)

                self.R(RStr, processingNotice=processing, wantType = 'NoConversion')
            else:
                if self.fileType.getChecked() ==_('Clipboard'):
                    settings = {'NEWDATA':self.Rvariables['dataframe_org'], 'FILENAME':'"clipboard"', 'HEADER':header, 'SEP':sep, 'QUOTE':unicode(self.quote.text()).replace('"','\\"'), 'COLCLASSES':ccl, 'PARAMNAME':param_name, 'SKIP':unicode(self.numLinesSkip.text()), 'NROWS':nrows, 'OTHER':otherOptions, 'DEC':unicode(self.decimal.text())}
                    
                else:
                    settings = {'NEWDATA':self.Rvariables['dataframe_org'], 'FILENAME':self.Rvariables['filename'], 'HEADER':header, 'SEP':sep, 'QUOTE':unicode(self.quote.text()).replace('"','\\"'), 'COLCLASSES':ccl, 'PARAMNAME':param_name, 'SKIP':unicode(self.numLinesSkip.text()), 'NROWS':nrows, 'OTHER':otherOptions, 'DEC':unicode(self.decimal.text())}
                
                RStr = '%(NEWDATA)s <- read.table(%(FILENAME)s, header = %(HEADER)s, sep = "%(SEP)s", quote = "%(QUOTE)s", colClasses = %(COLCLASSES)s, row.names = %(PARAMNAME)s, skip = %(SKIP)s, nrows = %(NROWS)s , dec = "%(DEC)s", %(OTHER)s)' % settings
                    
                self.R(RStr, processingNotice=processing, wantType = 'NoConversion')
                
        except:
            import redRLog
            redRLog.log(redRLog.REDRCORE, redRLog.WARNING,redRLog.formatException())
            self.rowNamesCombo.setCurrentIndex(0)
            self.updateScan()
            return
        
        self.updateScan()
        self.commit()

    def updateScan(self):
        if self.rowNamesCombo.count() == 0:
            self.colNames = self.R('colnames(' + self.Rvariables['dataframe_org'] + ')',wantType='list')
            self.rowNamesCombo.clear()
            self.rowNamesCombo.addItem('NULL','NULL')
            for x in self.colNames:
                self.rowNamesCombo.addItem(x,x)
        self.scanarea.clear()
        data = self.R('rbind(colnames(' + self.Rvariables['dataframe_org'] 
        + '), as.matrix(' + self.Rvariables['dataframe_org'] + '))',wantType='list')
        rownames = self.R('rownames(' + self.Rvariables['dataframe_org'] + ')',wantType='list')
        
        txt = self.html_table(data,rownames)
        self.scanarea.setText(txt)
            
        
        try:
            if len(self.colClasses) ==0:
                self.colClasses = self.R('as.vector(sapply(' + self.Rvariables['dataframe_org'] + ',class))',wantType='list')
                self.myColClasses = self.colClasses
                # print '@@@@@@@@@@@@@@@@@@@@@@@@@', self.myColClasses
            if len(self.dataTypes) ==0:
                types = ['factor','numeric','character','integer','logical']
                self.dataTypes = []
                
                for k,i,v in zip(range(len(self.colNames)),self.colNames,self.myColClasses):
                    s = redRGUI.base.radioButtons(self.columnTypes,label=i,displayLabel=False,
                    buttons=types,orientation='horizontal',callback=self.updateColClasses)
                    
                    # print k,i,unicode(v)
                    if unicode(v) in types:
                        s.setChecked(unicode(v))
                    else:
                        s.addButton(unicode(v))
                        s.setChecked(unicode(v))
                    label = redRGUI.base.widgetLabel(None,label=i)
                    self.columnTypes.layout().addWidget(label.controlArea,k,0)
                    self.columnTypes.layout().addWidget(s.controlArea,k,1)
                    
                    self.dataTypes.append([i,s])
        except:
            import redRLog
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            self.scanarea.clear()
            self.scanarea.setText(_('Problem reading or scanning the file.  Please check the file integrity and try again.'))
        
        # print self.getReportText('./')
          
    def html_table(self,lol,rownames):
        s = '<table border="1" cellpadding="3">'
        s+= _('  <tr><td>Rownames</td><td><b>')
        s+= '    </b></td><td><b>'.join(lol[0])
        s+= '  </b></td></tr>'
        
        for row, sublist in zip(rownames,lol[1:]):
            s+= '  <tr><td><b>' +row + '</b></td><td>'
            s+= '    </td><td>'.join(sublist)
            s+= '  </td></tr>'
        s+= '</table>'
        return s
        
    def updateGUI(self):
        dfsummary = self.R('dim('+self.Rvariables['dataframe_org'] + ')', wantType='list',silent=True)
        if self.fileType.getChecked() == _("Clipboard"):
            self.infob.setText('Clipboard')
        else:
            self.infob.setText(self.R(self.Rvariables['filename']))
        self.infoc.setText(_("Rows: %(ROWS)s\nColumns: %(COLS)s") % {'ROWS':unicode(dfsummary[0]), 'COLS':unicode(dfsummary[1])})
        self.FileInfoBox.setHidden(False)
    def commit(self):
        self.updateGUI()
        sendData = rdf.RDataFrame(self, data = self.Rvariables['dataframe_org'], parent = self.Rvariables['dataframe_org'])
        self.rSend("od1", sendData)
    
  