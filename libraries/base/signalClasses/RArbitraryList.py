## modelList, holds a list of data frames generated by the fold widget

from libraries.base.signalClasses.RVariable import *
from libraries.base.signalClasses.UnstructuredDict import *
from libraries.base.signalClasses.StructuredDict import *
import time

class RArbitraryList(RVariable, UnstructuredDict):
    convertFromList = [UnstructuredDict, StructuredDict]
    convertToList = [RVariable, UnstructuredDict]
    def __init__(self, widget, data, parent = None, checkVal = True):
        RVariable.__init__(self, widget = widget, data = data, parent = parent, checkVal = False)
        if checkVal and not self.R('is.list(%s)' % data):
            raise Exception
        self.newDataID = unicode(time.time()).replace('.', '_')
        
    def convertFromClass(self, signal):
        if isinstance(signal, UnstructuredDict):
            return self._convertFromUnstructuredDict(signal)
        elif isinstance(signal, StructuredDict):
            return self._convertFromStructuredDict(signal)
            
    def _convertFromStructuredDict(self, signal):
        newVar = self.assignR('RListConversion_'+self.newDataID, signal.getData())
        return RList(widget = self.widget, data = 'as.list('+newVar+')')
    def _convertFromUnstructuredDict(self, signal):
        newVar = self.assignR('RListConversion_'+self.newDataID, signal.getData())
        return RList(widget = self.widget, data = 'as.list('+newVar+')')
    def convertToClass(self, varClass):
        if varClass == RVariable:
            return self._convertToVariable()
        elif varClass == BaseRedRVariable:
            return self._convertToVariable()
        elif varClass == RArbitraryList:
            return self
        elif varClass == UnstructuredDict:
            return self._convertToUnstructuredDict()
        else:
            raise Exception
    def _convertToUnstructuredDict(self):
        return UnstructuredDict(widget = self.widget, data = self.R(self.getData(), wantType = 'dict'))
    def _convertToVariable(self):
        return self