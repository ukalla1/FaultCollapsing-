#including the library
import re

#initializing the function
def FILTER(INST):
	PIECES = re.split('[)]|[(]|[ ]|,|;|[.]Y\d{2}|[.]Y\d{1}.|[\n]|[.]Y|[.]A|[.]B', INST)
	return list(filter(None, PIECES ))

#to open the file to parse	
my_file = open ('C:/Users/uttej/Desktop/My Docs/Vesting Testing/Hw2/Hw2/Benchmark/c17.v', 'r')
inputArr = []
outputArr = []
my_file_lines = my_file.readlines();

#to perform the parsing on the entire the loop
for line in my_file_lines:
	split_arr = FILTER(line)
	identifier = split_arr[0]
	##print(split_arr)

	#to remove unnecessary lines	
	if 'module' not in identifier:
		print(split_arr)
		if identifier == 'input':
			inputArr = split_arr[1:]
		elif identifier == 'output':
			outputArr = split_arr[1:]


#to print the parsed output
print(inputArr)
print(outputArr)