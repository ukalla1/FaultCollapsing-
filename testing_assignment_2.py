

import re



def FILTER(INST):
    PIECES = re.split('[)]|[(]|[ ]|,|;|[.]Y\d{2}|[.]Y\d{1}.|[\n]|[.]Y|[.]A|[.]B', INST)
    return list(filter(None, PIECES))  
 


my_file = open ('C:/Users/uttej/Desktop/My Docs/VLSI Testing/Hw2/Benchmark/c499.v', 'r')

# arrays to hold input, output and wire values
inputArr = []
outputArr = []
wireArr = []
gateArr = []
fanoutArr = []
gateFanArr = []



my_file_lines = my_file.readlines()  
number_of_lines = len(my_file_lines)


uniqueList = []
loopIndex = -1
for line in my_file_lines:
    loopIndex = loopIndex + 1
    split_arr = FILTER(line)
    identifier = split_arr[0]
    if  'module' not in identifier and 'input' not in identifier and 'output' not in identifier and 'wire' not in identifier and 'fanout' not in identifier:
        gateArr.insert(loopIndex, split_arr)
        
    elif 'fanout' in identifier:
        fanoutArr.insert(loopIndex, split_arr)
                    
                    
        ##loading the inputs to an input arr
    if identifier == 'input':
        inputArr = split_arr[1:]
    elif identifier == 'output':
        outputArr = split_arr[1:]
    elif identifier == 'wire':
        wireArr = split_arr[1:]
    
gateFanArr.append(gateArr + fanoutArr)
# print(uniqueList)


unique = []
result = []
randomArr = []
unique.append(inputArr)
unique.append(outputArr)
unique.append(wireArr)
for gfInfo in gateFanArr[0]:
    for indexx in range(2, len(gfInfo)):
        info = gfInfo[indexx]
        if ((info in inputArr) or (info in outputArr) or (info in wireArr)):
            pass
        else:
            randomArr.append(info)
unique.append(randomArr)
countInfo = 0
out_file = open ('C:/Users/uttej/Desktop/My Docs/VLSI Testing/Hw2/Benchmark/test_inputbf.txt', 'w')
for g in unique:
    for gf in g:
        countInfo = countInfo+2
        out_file.write("Sa1   " + gf +"\n")
        out_file.write("Sa0   " + gf +"\n")
print(countInfo)
out_file.close()




def levelFunct(presentLevel, ip1, ip2, inputArr):


    if ip1 in inputArr and ip2 in inputArr:
        return 0
    elif ip1 in inputArr or ip2 in inputArr:
        return 1

    nextLevel = presentLevel + 1
    return nextLevel



dict_all = {'0' : [] , '1' : []}
presentLevel = 0 
for i in range(0, gateArr.__len__()):
        inputIdentifier = gateArr[i][0]
        current_Gate = gateArr[i]
        current_GateLength = len(current_Gate)
        #print(current_GateLength)
        input1 = current_Gate[3]
        if current_GateLength == 4:
            input2 = 0
        else:
            input2 = current_Gate[4]
        current_level = levelFunct(presentLevel, input1, input2, inputArr)
        presentLevel = current_level
        if(str(current_level) not in dict_all.keys() ):
            dict_all[str(current_level)] = [current_Gate[1]]
        else:    
            value = dict_all[str(current_level)]
            value.append(current_Gate[1])
            dict_all[str(current_level)] = value
# print(dict_all)



def removeOut(updatedGateInfo):
    aLength = len(updatedGateInfo)
    outputName = updatedGateInfo[2] # this will not change for any gate so hardcoded
    for index in range(0, len(gateArr)):
        gInfo = gateArr[index]
        gLength = len(gInfo)
        if ((gLength == 5 and (outputName in gInfo[3] or outputName in gInfo[4])) or (gLength ==4 and outputName in gInfo[3])):
#             
            if updatedGateInfo[0] == "NAND2X1" or updatedGateInfo[0] == "NOR2X1" or updatedGateInfo[0] == "OR2X1" or updatedGateInfo[0] == "AND2X1" or updatedGateInfo[0] == "XOR2X1":
               updatedGateInfo = updatedGateInfo[0:aLength-2]
            elif updatedGateInfo[0] == "INVX1" or updatedGateInfo[0] == "BUFX1":
                updatedGateInfo = updatedGateInfo[0:aLength-1]
            return updatedGateInfo
            
    return updatedGateInfo



gateFaults = []
fanoutFaults = []
newfanoutArr = []
faultCondition0 = 'X'
faultCondition2 = 'Sa0'
faultCondition3 = 'Sa1'
faultCondition4 = '0'
loopIndex = -1
for i in range (0, gateArr.__len__()):
    loopIndex = loopIndex + 1
    newGate = gateArr[i] + [faultCondition0]
    gateFaults.insert(loopIndex, newGate)


lIndex = -1
for i in range (0, fanoutArr.__len__()):
    lIndex = lIndex + 1
    newfanout = fanoutArr[i] + [faultCondition0]    
    fanoutFaults.insert(lIndex, newfanout)



def faultFunct(gateInfo):
    arrLength = len(gateInfo)
    
    for i in range(0, arrLength-1):
        if gateInfo[arrLength-1] == 'X':
            if gateInfo[0] == 'NAND2X1':
                # creating new list
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition3+'    '+gateInfo[3])
                gateInfo.append(faultCondition3+'    '+gateInfo[4])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
                gateInfo = removeOut(gateInfo)
#                 print(gateInfo)
            elif gateInfo[0] == 'INVX1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition3+'    '+gateInfo[3])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
                gateInfo = removeOut(gateInfo)
            elif gateInfo[0] == 'AND2X1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition3+'    '+gateInfo[3])
                gateInfo.append(faultCondition3+'    '+gateInfo[4])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
                gateInfo = removeOut(gateInfo)
            elif gateInfo[0] == 'OR2X1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition2+'    '+gateInfo[3])
                gateInfo.append(faultCondition2+'    '+gateInfo[4])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
                gateInfo = removeOut(gateInfo)
            elif gateInfo[0] == 'NOR2X1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition2+'    '+gateInfo[3])
                gateInfo.append(faultCondition2+'    '+gateInfo[4])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
                gateInfo = removeOut(gateInfo)
            elif gateInfo[0] == 'BUFX1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
#                 gateInfo.append(faultCondition2+'    '+gateInfo[3])
#                 gateInfo.append(faultCondition3+'    '+gateInfo[3])
                gateInfo = removeOut(gateInfo)
            elif gateInfo[0] == 'XOR2X1':
                gateInfo.remove(gateInfo[arrLength-1])
                gateInfo.append(faultCondition2+'    '+gateInfo[3])
                gateInfo.append(faultCondition3+'    '+gateInfo[3])
                gateInfo.append(faultCondition2+'    '+gateInfo[4])
                gateInfo.append(faultCondition3+'    '+gateInfo[4])
                gateInfo.append(faultCondition2+'    '+gateInfo[2])
                gateInfo.append(faultCondition3+'    '+gateInfo[2])
        else: 
            return gateInfo
        

def fanfaultFunct(fanInfo):

    fanLength = len(fanInfo)
    for k in range(0, fanLength-1):
        if fanInfo[fanLength-1] == 'X':
            if "fanout" in fanInfo[0]:
                fanInfo.remove(fanInfo[fanLength-1])
                fanInfo.append(fanInfo[2]+'    '+faultCondition2)
                fanInfo.append(fanInfo[2]+'    '+faultCondition3)
                return(fanInfo)
        else:
            return fanInfo


# In[13]:


collapsedGates = []
collapsedFans = []
aIndex = -1
for i in range (1, dict_all.__len__()):
    listAll = dict_all[str(i)]
    for j in range (0, listAll.__len__()):
            gateIndex = [(x, gates.index(listAll[j]))
                        for x, gates in enumerate(gateFaults)
                        if listAll[j] in gates]
            tempIndex = gateIndex[0]
            Index = tempIndex[0]
            gateInfo = gateFaults[Index]
            updatedgateInfo = faultFunct(gateInfo)
            if updatedgateInfo[0] == "INV2X1":
                newGates = updatedgateInfo[4:]
            else:
                newGates = updatedgateInfo[5:]
            collapsedGates.insert(aIndex, newGates)
                


for k in range(0, len(fanoutFaults)):
    updatedfanInfo = fanfaultFunct(fanoutFaults[k])
    originalFanInfo = fanoutArr[k]
    

    for fInfo in originalFanInfo:
        if fInfo in updatedfanInfo:
            updatedfanInfo.remove(fInfo)
    collapsedFans.append(updatedfanInfo)



collapsedFaults = [collapsedGates] + [collapsedFans]

count = 0
outputList = []
f = open('C:/Users/uttej/Desktop/My Docs/VLSI Testing/Hw2/Benchmark/output_test.txt', 'w')
cIndex = -1
for i in range(len(collapsedFaults)):
    for j in range(len(collapsedFaults[i])):
        for k in range(len(collapsedFaults[i][j])):
            cIndex = cIndex + 1
            f.write(str("%d  ->  %s"%(count, collapsedFaults[i][j][k])))
            f.write("\n")
            print("%d  ->  %s"%(count, collapsedFaults[i][j][k]))
            count+=1
f.write("\n")
f.write("Total Faults_AF = %d\n"%(count))
print(count)
collapseRatio = count / countInfo
print(collapseRatio)
f.write("\nthe collapse ratio is = %d/%d = %f"%(count, countInfo, collapseRatio))
f.close()



print (count)



