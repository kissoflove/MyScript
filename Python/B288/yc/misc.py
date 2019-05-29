# Copyright (C) 2017 Apple Inc. All rights reserved.
#
# This document is the property of Apple Inc.
# It is considered confidential and proprietary.
#
# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of
# Apple Inc.
#
# Created by Yewching Chen <yewching_chen@apple.com> 
#

import time
from datetime import datetime
import os
import errno

class output:	
	def __init__(self,filename,selectDateTime,selectPath,filepath):
		if selectDateTime:
			now = datetime.now()
			extension = "_{:%Y-%m-%d_%H-%M-%S}.txt".format(now)
			filename = filename + extension
		if selectPath:
			outputpath = valid_path(filepath)
			filename = os.path.join(outputpath,filename)
		self.__f = open(filename,'a')	
		
	def write(self,line):		
		print(line)
		self.__f.write(line)	
		self.__f.write('\n')
	
	def close(self):
		self.__f.close()		

	# csv_write([itemA,itemB,itemC])
	def csv_write(self, line):
		self.__f.write(', '.join([str(w) for w in line])+'\n')
		
def valid_path(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	return path	