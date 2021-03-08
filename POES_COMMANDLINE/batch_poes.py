import os
import time

path = os.getcwd()+'\input_files'
path_output =  os.getcwd()+'\output'

files = os.listdir(path)

for f in files:
    str  = "python poes.py -i input_files/" +f+ " -w wordlist.txt - r HR1,score_data_csv"
    #print(f,str)
    #print(os.getcwd())
    os.system(str)
    time.sleep(2)

outputfiles = os.listdir(path_output)
for f in outputfiles:
    if os.path.isfile(os.getcwd()+'\output\\'+f):
        os.remove(os.getcwd()+'\output\\'+f)
    
