import os
import time
from datetime import datetime
import re
import csv

path = os.getcwd()+'\subjects'
path_output =  os.getcwd()+'\output\output-CSV'
path_csv_input = os.getcwd()+'/CSV_Input/'

def readTSVInput():
    # Using readlines()
    files = os.listdir(path_csv_input)
    fileCount = 1
    #file_output = open(os.getcwd()+'/parsed_text.txt', 'w')
    for f in files:
        #file1 = open(path_csv_input+f, 'r',encoding="utf8") 
        with open(path_csv_input+f) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            counter = 0
            for line in tsvreader:
                line2 = str(line)
                if len(line2.replace('\t','').replace(',','').replace('"','').replace('\n',''))!=0:
                    counter = counter+1
                    print("ROW:",counter)                    
                    subcounter=1
                    #folder_name = "User"+str(counter)
                    if len(line[1:])>157 and counter >=2:
                        #file_output.write("ROW:"+str(counter))
                        #file_output.write('\n')
                        list_data = list( line[1:][i] for i in [115,120,125,130,135,140,145,150,155])
                        list_identifiers = list( line[1:][i] for i in [7,8,19,20])
                        #list_complete_data = list( line[0:][i] for i in range(len(line[1:])) if not i in [7,8,19,20,115,120,125,130,135,140,145,150,155])
                        #str_complete_data = ",".join(list_complete_data)
                        #print("str_complete_data",str_complete_data)
                        responseId = list_identifiers[0]
                        eLeasMatchID = list_identifiers[1]
                        age = list_identifiers[2]
                        gender = list_identifiers[3]
                        additionalInfo = responseId+":"+eLeasMatchID+":"+age+":"+gender
                        #list1 = list( line[1:][i] for i in [115])
                        for l in list_data:
                            #create input file and run POES here passing all the identifiers as well
                            l1= str(l)
                            if len(l1.replace('\t','').replace(',','').replace('"','').replace('\n',''))!=0:
                                #filename = "user_"+responseId+"_text_"+str(subcounter)+".txt";
                                filename = "User"+str(counter-1)+"_text"+str(subcounter)+".txt"
                                #create input file
                                inpfileLoc = createInputFile(filename,l.strip())
                                subcounter=subcounter+1
                                #call POES
                                _str  = "python poes.py -i input_files/" +inpfileLoc+ " -w wordlist.txt - r HR1,score_data_csv -p "+additionalInfo
                                os.system(_str)
                                time.sleep(1)
                                #deleteExtraFile(os.getcwd()+'\\output\\'+"User"+str(counter-4))
                                #delete inputfile
                                #os.remove(inpfileLoc)
                            #file_output.write(list_identifiers[0]+":"+list_identifiers[1]+":"+list_identifiers[2]+":"+list_identifiers[3]);
                            #file_output.write('\n')
                            #file_output.write(str(l))
                            #file_output.write('\n')
                print("*"*10)
                #file_output.write("*******************")
                #file_output.write('\n')
    #file_output.close()


def createInputFile(filename,txt):
    file_output = open(os.getcwd()+'/input_files/'+filename, 'w')
    file_output.write('1')
    file_output.write('\n')
    file_output.write('101,1,1,"'+txt+'"')
    file_output.close()
    #return os.getcwd()+'/input_files/'+filename
    return filename

def clearTempInputFiles():
    path_temp_input =  os.getcwd()+'/input_files'
    temp_inputfiles = os.listdir(path_temp_input)
    for f in temp_inputfiles:
        if os.path.isfile(os.getcwd()+'\input_files\\'+f):
            os.remove(os.getcwd()+'\input_files\\'+f)

def deleteExtraFile(folder):
    temp_inputfiles = os.listdir(folder)
    for f in temp_inputfiles:
        if "score_data_csv" in f:
            os.remove(folder+'\\'+f)
    
def combineCSVOutput():
    now = time.time()
    files = os.listdir(path_output)
    fileCount = 1
    QuestionIndex = 0
    QuestionTitles = ["1.1_Rand-Tennis_Q","1.2_GD-Fight_Q","1.3_ToM-Surprise_Q","2.1_GD-Follow_Q","2.2_ToM-Coaxing_Q","2.3_Rand-Star_Q","3.1_ToM-Mocking_Q","3.2_Rand-Drift_Q","3.3_Chasing_Q"]
    file_output = open(os.getcwd()+'\CombinedCSV_'+str(now).split('.')[0]+'.csv', 'w') 
    for f in files:
        file1 = open("output/output-CSV/"+f, 'r')
        Lines = file1.readlines()
        if "Combine" not in f:
            if fileCount==1 :
                #print("Line{}: {}".format(20, Lines[20].strip()))
                file_output.write("SUBJECT FILE,QUESTION_TITLE,"+Lines[20].strip())
                file_output.write("\n")
                #print("Line{}: {}".format(21, Lines[21].strip()))
                #file_output.write(f+","+Lines[21].strip())
                file_output.write(f+","+QuestionTitles[QuestionIndex]+","+Lines[21].strip())
                file_output.write("\n")
            else:
                #print("Line{}: {}".format(21, Lines[21].strip()))
                #print(QuestionIndex,QuestionTitles[QuestionIndex])
                file_output.write(f+","+QuestionTitles[QuestionIndex]+","+Lines[21].strip())
                file_output.write("\n")

            if QuestionIndex>=8:
                QuestionIndex = 0
            else:
                QuestionIndex = QuestionIndex+1
            fileCount = fileCount+1
    file_output.close()
    print("Combined CSV Output file generated")

def editCSVOutput():
    now = time.time()
    fileCount = 1
    file_output = open(os.getcwd()+'\CombinedCSV_3'+'.csv', 'a') 
    #for f in files:
    file1 = open("CombinedCSV_1.csv", 'r')
    Lines = file1.readlines()
    linecounter = 0
    for l in Lines:
        if linecounter ==0 or (linecounter%2!=0):
            file_output.write(l.strip())
            file_output.write("\n")
        linecounter = linecounter+1
    file_output.close()
    print("Combined CSV Output file generated")    

def executeBatchPoes():
    str  = "python batch_poes.py"
    os.system(str)

def clearOutputFiles():
    output_path = os.getcwd()+'\\output\\'
    outputfiles = os.listdir(output_path)
    for f in outputfiles:
        if os.path.isfile(os.getcwd()+'\output\\'+f):
            os.remove(os.getcwd()+'\output\\'+f)



clearTempInputFiles()
readTSVInput()
##clearTempInputFiles()
##executeBatchPoes()#commented as executing POES on each input line read
#combineCSVOutput() #commented as moved this code to score_data_csv.py file
clearOutputFiles()
editCSVOutput()
