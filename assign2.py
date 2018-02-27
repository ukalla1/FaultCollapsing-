import os
import re

def FILTER(INST):
 PIECES = re.split('[)]|[(]|[ ]|,|;|[.]Y20|[.]Y19|[.]Y18|[.]Y17|[.]Y16|[.]Y15|[.]Y14|[.]Y13|[.]Y12|[.]Y11|[.]Y10|[.]Y9|[.]Y8|[.]Y7|[.]Y6|[.]Y5|[.]Y4|[.]Y3|[.]Y2|[.]Y1|[.].', INST_CURR)
 return list(filter(None, PIECES))  
 
 
 
 example = FILTER  ("NAND2X1 uut192 (.Y1(N520),.A(N495fo0),.B(N207fo0));")
 
 print(example)