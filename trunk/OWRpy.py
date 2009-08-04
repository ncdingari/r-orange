#
# An Orange-Rpy class
# 
# Should include all the functionally need to connect Orange to R 
#

from OWWidget import *
from rpy import *

class OWRpy():
	#a class variable which is incremented every time OWRpy is instantiated.
	
	num_widgets = 0
	def __init__(self):	
		#The class variable is used to create the unique names in R
		OWRpy.num_widgets += 1
		#this should be appended to every R variable
		self.variable_suffix = '_' + str(OWRpy.num_widgets)
		#create easy access to the R object
		
		
	#convert R data.frames to Orange exampleTables
	def convertDataframeToExampleTable(self, dataFrame_name):
		dataFrame = r[dataFrame_name]
		col_names = r.colnames(dataFrame)
		col_def = r.sapply(dataFrame,'class')

		colClasses = []
		for i in col_names:
			if col_def[i] == 'numeric' or col_def[i] == 'integer':
				colClasses.append(orange.FloatVariable(i))
			elif col_def[i] == 'factor':
				colClasses.append(orange.StringVariable(i))
			elif col_def[i] == 'character':
				colClasses.append(orange.StringVariable(i))



		d = r('as.matrix(d1)')
		domain = orange.Domain(colClasses)
		data = orange.ExampleTable(domain, d)		
		return data
		