# Start of the Fuzzy Logic Part
#To write console Output in a text file and save it in a given path
import sys

#A function done to catch error while reading from input file to end the program in a nice way
def readline(readFilePath,line): 

   try:
       line = readFilePath.readline()
       print(line)
       return line

   except IOError:
        print("Error in file reading, exit program")
        sys.stdout.close()
        return -1
                      
#Fuzzification Function
#Sample Output
#result = [[['beginner', 0.0], ['intermediate', 0.3333333333333335], ['expert', 0.33333333333333326]], [['very_low', 0.0], ['low', 0.5], ['medium', 0.5], ['high', 0.0]]]
def Fuzzification(inputVars,inputVarsRange,inputFuzzySetNames,inputFuzzySetTypes,inputFuzzySetValues,inputVarsVals):

   result = []

   for i in range(len(inputVars)):

       result_i =[]

       if((inputVarsVals[i] >= inputVarsRange[i][0]) and (inputVarsVals[i] <= inputVarsRange[i][1])):
           
           for j in range(len(inputFuzzySetTypes[i])):

               result_y = 0.0
               slope = 0.0
               intercept = 0.0
               point1 =[] 
               point2 =[]
               point3 =[]
               point4 =[]

               if(inputFuzzySetTypes[i][j].lower() == "tri"): 

                   point1 = [inputFuzzySetValues[i][j][0] ,0]
                   point2 = [inputFuzzySetValues[i][j][1] ,1]
                   point3 = [inputFuzzySetValues[i][j][2] ,0]

                   if(inputVarsVals[i] >= point1[0] and inputVarsVals[i]<=point2[0]):
                       try:
                          slope = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
                          intercept = float(point1[1]) - float(point1[0] * slope)
                          result_y = float(inputVarsVals[i] * slope ) + float(intercept)
                       except ZeroDivisionError:
                           result_y = 1

                   elif(inputVarsVals[i] >= point2[0] and inputVarsVals[i]<=point3[0]):
                       try:
                          slope = float(point3[1] - point2[1]) / float(point3[0] - point2[0])
                          intercept = float(point2[1]) - float(point2[0] * slope)
                          result_y = float(inputVarsVals[i] * slope ) + float(intercept)
                       except ZeroDivisionError:
                           result_y = 1

               if(inputFuzzySetTypes[i][j].lower() == "trap"):
                   point1 = [inputFuzzySetValues[i][j][0] ,0]
                   point2 = [inputFuzzySetValues[i][j][1] ,1]
                   point3 = [inputFuzzySetValues[i][j][2] ,1]
                   point4 = [inputFuzzySetValues[i][j][3] ,0]

                   if(inputVarsVals[i] >= point1[0] and inputVarsVals[i]<=point2[0]):
                       try:
                          slope = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
                          intercept = float(point1[1]) - float(point1[0] * slope)
                          result_y = float(inputVarsVals[i] * slope ) + float(intercept)
                       except ZeroDivisionError:
                           result_y = 1

                   elif(inputVarsVals[i] >= point2[0] and inputVarsVals[i]<=point3[0]):
                       try:
                           slope = float(point3[1] - point2[1]) / float(point3[0] - point2[0])
                           intercept = float(point2[1]) - float(point2[0] * slope)
                           result_y = float(inputVarsVals[i] * slope ) + float(intercept)
                       except ZeroDivisionError:
                            result_y = 1
                  
                   elif(inputVarsVals[i] >= point3[0] and inputVarsVals[i] <= point4[0]):
                      try:
                         slope = float(point4[1] - point3[1]) / float(point4[0] - point3[0])
                         intercept = float(point3[1] - float(point3[0]*slope))
                         result_y = float(inputVarsVals[i] * slope ) + float(intercept)
                      except ZeroDivisionError:
                          result_y = 1

               result_i.append([inputFuzzySetNames[i][j],result_y])
            
       result.append(result_i)

   return result

#Inference Function
#Sample Output
#Myresult = {'risk': [['high', 0.0], ['high', 0.0], ['low', 0.33333333333333326], ['normal', 0.0], ['normal', 0.3333333333333335]]}
#result = [[['beginner', 0.0], ['intermediate', 0.3333333333333335], ['expert', 0.33333333333333326]], [['very_low', 0.0], ['low', 0.5], ['medium', 0.5], ['high', 0.0]]]
#rule[i] = 'proj_funding high or exp_level expert => risk low'
def Inference(rules,result,inputVars,outputVars,outputFuzzySetsNames):

    Myresult = {}
    arr = []
    for i in range(len(rules)):

        value = 0 
        temp = rules[i].split(" ")
        indexVar1 = indexVar2 =  var1Set1 = var2Set2 = indexOut =  ValOut = 0
        Val1 = Val2 =  ""

        try:
           indexVar1 = inputVars.index(temp[0],0,len(inputVars))
           indexVar2 = inputVars.index(temp[3],0,len(inputVars)) 
           indexOut = outputVars.index(temp[6],0,len(outputVars))
           Val1 = temp[1]
           Val2 = temp[4]
           ValOut = outputFuzzySetsNames[indexOut].index(temp[7],0,len(outputFuzzySetsNames[indexOut]))
           temp1 =[result[indexVar1][i][0] for i in range(len(result[indexVar1]))]
           temp2 =[result[indexVar2][i][0] for i in range(len(result[indexVar2]))]
           var1Set1 = temp1.index(Val1,0,len(temp1))
           var2Set2 = temp2.index(Val2,0,len(temp2))           

        except ValueError:
           print(f"Error wrong rules format entered in rule number {i+1}, exit system.")
           sys.stdout.close()
           return Myresult

        if(temp[2] == "or"):
            value = max(result[indexVar1][var1Set1][1],result[indexVar2][var2Set2][1])

        elif(temp[2] == "and"):
            value = min(result[indexVar1][var1Set1][1],result[indexVar2][var2Set2][1])

        elif(temp[2] == "and_not"):
            value = min(result[indexVar1][var1Set1][1],1.0 - result[indexVar2][var2Set2][1])

        elif(temp[2] == "or_not"):
            value = max(result[indexVar1][var1Set1][1],1.0 - result[indexVar2][var2Set2][1])

        else:
           print("Error wrong rules format entered, exit system.")
           sys.stdout.close()
           return Myresult
        
        flag = False
        if(len(arr) == 0 ): 

            arr.append([outputVars[indexOut],temp[7],value])
            flag= True
  
        else:
            for j in range(len(arr)):

                if(temp[6] == arr[j][0]):

                    if(temp[7] == arr[j][1]):
                        arr[j][2] = arr[j][2] + value
                        flag = True

        if(flag == False):
            arr.append([outputVars[indexOut],temp[7],value])

        if(temp[6] in inputVars):
                index = inputVars.index(temp[6],0,len(inputVars)) 
                result[index][ValOut][1] = value
    
    arr.sort()
    res = tuple(tuple((sub[0],sub[1:]),)for sub in arr)
    
    temp = []

    for i in range(len(res)-1):

        if(res[i][0] == res[i+1][0]):
            if(res[i][1] not in temp):
                  temp.append(res[i][1])
            temp.append(res[i+1][1])     
        else:
            if(temp == []):
               temp.append(res[i][1])
            else:
               Myresult[res[i][0]] = temp 
               temp = []

    Myresult[res[i][0]] = temp 

    return Myresult 

#Deffuzification
#result = {'risk': [['high', 0.0], ['high', 0.0], ['low', 0.33333333333333326], ['normal', 0.0], ['normal', 0.3333333333333335]]}
#outputFuzzySetsValues = [[[0, 25, 50], [25, 50, 75], [50, 100, 100]]]
#outputFuzzySetNames = [['low', 'normal', 'high']]
#outputVars = ['risk']
#centroids = {'risk': [['low', 25.0], ['normal', 50.0], ['high', 83.33333333333333]]}
#Sample Output = fuzzyOutput = {'risk': 37.50000000000001}
def Defuzzification(result,outputVars,outputFuzzySetValues,outputFuzzySetsNames,outputFuzzySetTypes,outputVarsRanges,inputVars):
    
    centroids = {}
    fuzzyOutput = {}

    for i in range(len(outputVars)): 

        if(outputVars[i] in inputVars):

            del outputVars[i]
            del outputFuzzySetValues[i]
            del outputFuzzySetsNames[i]
            del outputFuzzySetTypes[i]
            del outputVarsRanges[i]
            break

    
    for i in range(len(outputVars)):

        arr = []

        for j in range(len(outputFuzzySetsNames[i])):

            sumValues = 0.0

            for m in range(len(outputFuzzySetValues[i][j])):

                sumValues = sumValues + outputFuzzySetValues[i][j][m] 

            sumValues = sumValues / float(len(outputFuzzySetValues[i][j]))
            arr.append([outputFuzzySetsNames[i][j],sumValues] )

        centroids[outputVars[i]] = arr

    for i in result.items():

        result_key = i[0]
        if(result_key in inputVars):
            continue

        result_value = i[1]

        sumWeights = 0
        setResult = 0
        centroid_value = centroids[result_key]

        for j in range(len(centroid_value)):

            setName = centroid_value[j][0] 
            setValue = 0
            setCentroid = centroid_value[j][1]

            for m in range(len(result_value)):

                if(result_value[m][0] == setName):
                    setValue = setValue + result_value[m][1]
                   
            setResult = (setValue * setCentroid) + setResult
            sumWeights = sumWeights + setValue

        output_i = setResult / sumWeights
        fuzzyOutput[result_key] = output_i

    return fuzzyOutput

#printOutput Function for formatting output
#New_result = [[['low', 0.4999999999999998], ['normal', 0.5000000000000002], ['high', 0.0]]]
#The predicted risk is normal (37.5)
def printOutput(result,outputVars,outputVarsRange,outputFuzzySetNames,outputFuzzySetValues,outputFuzzySetTypes,sysName,sysDescription):

   outputVarsVals = list(result.values())
   New_result = Fuzzification(outputVars,outputVarsRange,outputFuzzySetNames,outputFuzzySetTypes,outputFuzzySetValues,outputVarsVals)
   
   print("\n:::FUZZY_SYSTEM_:::\n")
   print(sysName)
   print(sysDescription)

   for i in range(len(New_result)):

       res = list(tuple(sub) for sub in New_result[i])
       #sort list of tuples by second element (ascending order)
       sorted_res = sorted(res,key=lambda t: t[1])
       Final_output = "\nThe predicted " + outputVars[i] + " is " + sorted_res[-1][0] + " " + " ( " + str(round(result[outputVars[i]],3))+ " ) \n" 
       return Final_output

#SubMain function that reads the files lines and other functions
#print(inputVars)
#['proj_funding', 'exp_level']
#print(outputVars)
#['risk']
#print(inputVarsRange) 
#[[0, 100], [0, 60]]
#print(outputVarsRange)                 
#[[0, 100]]
#print(inputFuzzySetNames) 
#[['beginner', 'intermediate', 'expert'], ['very_low', 'low', 'medium', 'high']]
#print(inputFuzzySetTypes)                 
#[['TRI', 'TRI', 'TRI'], ['TRAP', 'TRAP', 'TRAP', 'TRAP']]
#print(inputFuzzySetValues) 
#[[[0, 15, 30], [15, 30, 45], [30, 60, 60]], [[0, 0, 10, 30], [10, 30, 40, 60], [40, 60, 70, 90], [70, 90, 100, 100]]]
#print(outputFuzzySetNames)
#[['low', 'normal', 'high']]
#print(outputFuzzySetTypes)  
#[['TRI', 'TRI', 'TRI']]
#print(outputFuzzySetValues) 
#[[[0, 25, 50], [25, 50, 75], [50, 100, 100]]]
#print(rules) 
#['proj_funding high or exp_level expert => risk low', 'proj_funding medium and exp_level intermediate => risk normal', 'proj_funding medium and exp_level beginner => risk normal', 'proj_funding low and exp_level beginner => risk high', 'proj_funding very_low and_not exp_level expert => risk high']
#print(inputVarsVals)
#[50, 40]
def SubMain(line,readFilePath,sysName,sysDescription):
    
    inputVars = []
    outputVars = []
    inputVarsRange = []
    outputVarsRange =[] 
    flag1 = False
    inputFuzzySetNames = []
    inputFuzzySetTypes = [] 
    inputFuzzySetValues = []
    outputFuzzySetNames = []
    outputFuzzySetTypes = [] 
    outputFuzzySetValues = []
    rules = []
    inputVarsVals= []
    new_input_vars = []
    new_output_vars = []

    result =""

    while(line):

        print("Main Menu:")
        print("==========")
        print("1- Add variables.")
        print("2- Add fuzzy sets to an existing variable.")
        print("3- Add rules.")
        print("4- Run the simulation on crisp values.")
        print("5- Or Enter ::: Close")
        line = readline(readFilePath,line)

        try:
            line = int(line)

        except ValueError:
            if(line.lower().rstrip() != "close"):
               print("Error ,Enter only from 1:4 or Close ,exit program.")
               sys.stdout.close()
               return -1   
            else:
                return result

        if(int(line) == 1):

            print("Enter the variable\'s name, type (IN/OUT) and range ([lower,upper]):")
            print("EXAMPLE::: myVariable IN [0,100]")
            print("(Press x to finish)")
            line = readline(readFilePath,line)

            while(line[0].lower() != "x" and line[1]!="\n"):

                temp = line.split(" ")
                
                if(temp[1].lower() == "in"):
                    inputVars.append(temp[0])
                    myRange = (temp[2])[1:-2]
                    myRange = myRange.split(",")
                    varRange = []
                    varRange.append(int(myRange[0]))
                    varRange.append(int(myRange[1]))
                    inputVarsRange.append(varRange)

                elif(temp[1].lower() == "out"):
                    outputVars.append(temp[0])
                    myRange = (temp[2])[1:-2]
                    myRange = myRange.split(",")
                    varRange = []
                    varRange.append(int(myRange[0]))
                    varRange.append(int(myRange[1]))
                    outputVarsRange.append(varRange)

                else:
                    print("Error in your input format, exit program.")
                    sys.stdout.close()
                    return -1
                
                line = readline(readFilePath,line)

            flag1 = True

        elif(int(line) == 2):

            if(flag1 == False):

                print("CAN\'T START THE SIMULATION! Please add the fuzzy sets and rules first, exit program.")
                sys.stdout.close()
                return -1

            else:

                print("Enter the variable\'s name:")
                print("--------------------------")
                line = readline(readFilePath,line)
                indexVal = 0
                in_OR_out_flag = 0
     
                try:
                   indexVal = inputVars.index(line[:-1],0,len(inputVars))
                except ValueError:
                    try:
                         indexVal = outputVars.index(line[:-1],0,len(outputVars))
                         in_OR_out_flag = 1
                    except ValueError:
                         print("That variable does not exist in the system, exit program")
                         sys.stdout.close()
                         return -1
                
                variable = line[:-1]

                print("Enter the fuzzy set name, type (TRI/TRAP) and values: (Press x to finish)")
                print("EXAMPLE::: SetName TRI 0 20 30")
                print("EXAMPLE::: SetName TRAP 0 20 30 40")
                print("-----------------------------------------------------")
                line = readline(readFilePath,line)

                INnames = []
                INtypes =[]
                INvalues =[]
                OUTnames = []
                OUTtypes = []
                OUTvalues = []

                if(in_OR_out_flag == 0):
                    while(line[0].lower() != "x" and line[1]!="\n"):
                       temp = line.split(" ")
                       INnames.append(temp[0])
                       INtypes.append(temp[1])
                       INvalues.append(list(int(x) for x in temp[2:]))
                       line = readline(readFilePath,line)

                    inputFuzzySetNames.append(INnames)
                    inputFuzzySetTypes.append(INtypes)
                    inputFuzzySetValues.append(INvalues)
                    new_input_vars.append(variable)
                
                if(variable in outputVars and variable in inputVars): 
                    outputFuzzySetNames.append(INnames)
                    outputFuzzySetTypes.append(INtypes)
                    outputFuzzySetValues.append(INvalues)
                    new_output_vars.append(variable)

                if(in_OR_out_flag == 1):
                    while(line[0].lower() != "x" and line[1]!="\n"):
                       temp = line.split(" ")
                       OUTnames.append(temp[0])
                       OUTtypes.append(temp[1])
                       OUTvalues.append(list(int(x) for x in temp[2:]))
                       line = readline(readFilePath,line)

                    outputFuzzySetNames.append(OUTnames)
                    outputFuzzySetTypes.append(OUTtypes)
                    outputFuzzySetValues.append(OUTvalues)
                    new_output_vars.append(variable)

        elif(int(line) == 3):

             if(flag1 == False):

                print("CAN\'T START THE SIMULATION! Please add the fuzzy sets and rules first, exit program.")
                sys.stdout.close()
                return -1

             elif((len(inputVars) + len(outputVars) ) != (len(inputFuzzySetNames) + len(outputFuzzySetNames))):

                print("CAN\'T START THE SIMULATION! Please add the fuzzy sets names , types and values first ,exit program.")
                sys.stdout.close()
                return -1

             else:
                
                print("Enter the rules in this format: (Press x to finish)")
                print("IN_variable set operator IN_variable set => OUT_variable set")
                print("EXAMPLE::: x high or y medium => z low")
                print("------------------------------------------------------------")
                line = readline(readFilePath,line)

                while(line[0].lower() != "x" and line[1]!="\n"):
                    rules.append(line.rstrip())
                    line = readline(readFilePath,line)

        elif(int(line) == 4):

            if(flag1 == False):

                print("CAN\'T START THE SIMULATION! Please add the fuzzy sets and rules first, exit program.")
                sys.stdout.close()
                return -1

            elif((len(inputVars) + len(outputVars) ) != (len(inputFuzzySetNames) + len(outputFuzzySetNames))):

                print("CAN\'T START THE SIMULATION! Please add the fuzzy sets names , types and values first ,exit program.")
                sys.stdout.close()
                return -1

            elif(len(rules)==0):

               print("CAN\'T START THE SIMULATION! Please add the fuzzy rules first ,exit program.")
               sys.stdout.close()
               return -1

            else:

               print("Enter the crisp values:")
               print("-----------------------")

               for i in inputVars: 

                  if(i in outputVars):
                      inputVarsVals.append(0)

                  else:
                      print(i+" : ",end ='')
                      line = readline(readFilePath,line)
                      inputVarsVals.append(int(line))
               
               new_input_vars_vals = [i for i in inputVarsVals] 

               if(inputVars != new_input_vars):

                   for i in range(len(inputVars)):

                       index = new_input_vars.index(inputVars[i],0,len(new_input_vars)) 
                       new_input_vars_vals[index] = inputVarsVals[i]

               inputVars = new_input_vars
               outputVars = new_output_vars
               inputVarsVals = new_input_vars_vals
               print("Running the simulation...")
               result = Fuzzification(inputVars,inputVarsRange,inputFuzzySetNames,inputFuzzySetTypes,inputFuzzySetValues,inputVarsVals)
               print("Fuzzification => done")
               result = Inference(rules,result,inputVars,outputVars,outputFuzzySetNames)
               if(result == {}):
                   sys.stdout.close()
                   return -1
               else:
                   print("Inference => done")
                   result = Defuzzification(result,outputVars,outputFuzzySetValues,outputFuzzySetNames,outputFuzzySetTypes,outputVarsRange,inputVars)
                   print("Defuzzification => done")
                   result= printOutput(result,outputVars,outputVarsRange,outputFuzzySetNames,outputFuzzySetValues,outputFuzzySetTypes,sysName,sysDescription)
                   print(result)

#Main function that handles files and calles other functions 
def Main(readFilePath, writeFilePath):

    readFilePath = open(readFilePath) 

    sys.stdout = open(writeFilePath, "w")
    
    Final_output =""

    while(True):

       print("Fuzzy Logic Toolbox")
       print("===================")
       print("1- Create a new fuzzy system")
       print("2- Quit")

       line = readFilePath.readline()[:-1]
       print(line)

       if(int(line) == 1):

            print("Enter the system\'s name and a brief description:")
            print("------------------------------------------------")
            line = readline(readFilePath,line)
            sysName = line[:-1]
            line = readline(readFilePath,line)
            sysDescription = line[:-1] 
            Final_output = SubMain(line,readFilePath,sysName,sysDescription)
            sys.stdout.close()
            return Final_output, sysName, sysDescription
        
       elif (int(line) == 2):

            readFilePath.close()
            sys.stdout.close()
            sys.exit()

       else:

            print("Incorrect Choice ,you have to choose 1 or 2 only not to enter " + str(line))
            readFilePath.close()
            return -1
            

#End of Fuzzy logic part
#Start of GUI Part
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Doctork .ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

class Ui_MainWindow(object):

    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 90, 995, 471))
        self.label.setText("")
        self.label.setObjectName("label")

        self.welcom = QtWidgets.QLabel(self.centralwidget)
        self.welcom.setGeometry(QtCore.QRect(0, 0, 995, 91))

        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)

        self.welcom.setFont(font)
        self.welcom.setStyleSheet("\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.welcom.setAlignment(QtCore.Qt.AlignCenter)
        self.welcom.setObjectName("welcom")

        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        self.Description = QtWidgets.QLabel(self.centralwidget)
        self.Description.setFont(font)
        self.Description.setGeometry(QtCore.QRect(0, 10, 800, 500))
        self.Description.setObjectName("Description")

        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)

        self.uploadbutton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda:self.button_clicker())
        self.uploadbutton.setGeometry(QtCore.QRect(580, 410, 400, 45))

        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.uploadbutton.setFont(font)
        self.uploadbutton.setObjectName("Choose2Files")

        self.predictionlabrl = QtWidgets.QLabel(self.centralwidget)
        self.predictionlabrl.setGeometry(QtCore.QRect(0, 460, 1000, 101))

        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(25)

        self.predictionlabrl.setFont(font)
        self.predictionlabrl.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.predictionlabrl.setText("")
        self.predictionlabrl.setAlignment(QtCore.Qt.AlignCenter)
        self.predictionlabrl.setObjectName("predictionlabrl")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 410, 550, 41))
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n""font: 75 16pt \"Sakkal Majalla\";")
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 878, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.welcom.setText(_translate("MainWindow", "Simple Fuzzy Logic Tool Box"))
        self.uploadbutton.setText(_translate("MainWindow", "Choose Your Input then Output File"))
        self.label_2.setText(_translate("MainWindow", "Result will be here and Output File will be saved to its directory"))

    # action taken when button is clicked
    def button_clicker(self):

        import os
        os.chdir("C:\\Users\\Sarah Hesham\\OneDrive\\Documents\\Python\\GeneticAlgorithms_FuzzyLogicToolBox_GUI")

        input_file = QFileDialog.getOpenFileName()
        output_file = QFileDialog.getOpenFileName()

        if input_file[0] != '' and output_file[0] != '':

            try:
                output,sysName,sysDescription = Main(input_file[0],output_file[0])
                temp = sysDescription.split(" ")
                self.Description.setText(sysName+ " : "+"\n--------------------------------------"+"\n" + ' '.join(temp[0:int(len(temp)/3)]) + "\n" + ' '.join(temp[int(len(temp)/3):(int(len(temp)/3)+int(len(temp)/3))])+ "\n" + ' '.join(temp[(int(len(temp)/3)+int(len(temp)/3)):]))
                
                try:
                    output = int(output)
                    self.Description.setText("Unreadable File == Unknown")
                    self.predictionlabrl.setText("Error in Input File Format, Check Output File to know error details.")
           
                except ValueError:
                    self.predictionlabrl.setText(output)
            
            except ValueError:
                self.Description.setText("Unreadable File == Unknown")
                self.predictionlabrl.setText("Error in Input File Format, Completely wrong file")

        else:
            self.predictionlabrl.setText("Error Inappropriate Files Choosen")

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


#End of the GUI part
#End of code