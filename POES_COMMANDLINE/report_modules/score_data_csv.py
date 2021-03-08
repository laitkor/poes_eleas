# This reporting module outputs the score data as comma-separated values
# using the score data output file format from 1.x.x versions of POES
# (-d option in previous versions)

import os
from poes_heirarchy import *
from poes_wordlist import Wordlist
import time
from datetime import datetime

def report(batch, wordlist, outDir, outPrefix, configInfo, runid, additionalInfo):
    
    outLoc = (configInfo["SUBJFILELOC"].split('/')[1]).split('.')[0]
    print("Additional Info Score Data CSV", additionalInfo)
    responseId = additionalInfo.split(':')[0]
    eLeasMatchId = additionalInfo.split(':')[1]
    age = additionalInfo.split(':')[2]
    gender = additionalInfo.split(':')[3]
    #print("outLOC",outLoc)
    fileLoc = os.path.join(outDir, outPrefix + "_" + outLoc + ".csv")
    now = time.time()
    combineCSV = open(os.getcwd()+'\CombinedCSV_1'+'.csv', 'a')
    sf = open(fileLoc,"w")
    try:
        sf.write("\"Generated by POES Version " + configInfo["POES_VER"] + "\"\n\n")
        sf.write("\"APA style reference for POES:\"\n\"" + configInfo["POES_REF"] + "\"\n\n")
        sf.write("\"Wordlist Information:\"\n\"" + configInfo["WL_INFO"] + "\"\n\n")
        sf.write("\"APA style reference for Wordlist:\"\n\"" + configInfo["WL_REF"] + "\"\n\n")
        sf.write("\"Subject response data file name:\"\n\"" + configInfo["SUBJFILELOC"] + "\"\n\n")
        sf.write("\"Number of subjects:\"," + configInfo["NSUBJ"] + "\n\n")
        sf.write("\"Max. number of items:\"," + configInfo["MAXNITEMS"] + "\n\n")
        sf.write("\"Max. number of subparts:\"," + configInfo["MAXNSUBP"] + "\n\n")
    
        score_names = []


        # build lists of all the item IDs, subp IDs, and scoring method names 
        # in the order they appear 
        subjects = batch.getSubScorables()
        for subjID in batch.getSubIDOrder():
            items = subjects[subjID].getSubScorables()
            for itemID in subjects[subjID].getSubIDOrder():
                subparts = items[itemID].getSubScorables()
                for subpID in items[itemID].getSubIDOrder():
                    scoreTab = subparts[subpID].getScoreTable()
                    for methID in subparts[subpID].getScoreMethOrder():
                        name = "i" + itemID + "s" + subpID + "m" + methID
                        if name not in score_names:
                            score_names += [name]
                scoreTab = items[itemID].getScoreTable()
                for methID in items[itemID].getScoreMethOrder():
                    name = "i" + itemID + "m" + methID
                    if name not in score_names:
                        score_names += [name]
            scoreTab = subjects[subjID].getScoreTable()
            for methID in subjects[subjID].getScoreMethOrder():
                name = "m" + methID
                if name not in score_names:
                    score_names += [name]


        # create and write variable names line to output file
        #sf.write("SUBJECT FILE")
        combineCSV.write("SUBJECT FILE,")
        combineCSV.write("subjID")
        sf.write("subjID")
        for name in score_names:
            sf.write(',' + name)
            combineCSV.write(',' + name)
        sf.write(',responseId,eLeasMatchId,age,gender')#added on 9 November to include additional Info requested by Prof Lane. Code by Zain Islam
        sf.write('\n')
        combineCSV.write(',responseId,eLeasMatchId,age,gender')#added on 25 November to write values in Combined CSV Code by Zain Islam 
        combineCSV.write('\n')

        # for each subject make a dict with keys from (ism_names, im_names, m_names)
        # and values all '.'
        # fill in the values with scores where applicable
        subjData = dict.fromkeys(subjects.keys())
        for subjID in subjects:
            subjData[subjID] = dict.fromkeys(score_names, '.')
            items = subjects[subjID].getSubScorables()
            for itemID in items:
                subparts = items[itemID].getSubScorables()
                for subpID in subparts:
                    scoreTab = subparts[subpID].getScoreTable()
                    for methID in scoreTab:
                        name = "i" + itemID + "s" + subpID + "m" + methID
                        subjData[subjID][name] = scoreTab[methID]
                scoreTab = items[itemID].getScoreTable()
                for methID in scoreTab:
                    name = "i" + itemID + "m" + methID
                    subjData[subjID][name] = scoreTab[methID]
            scoreTab = subjects[subjID].getScoreTable()
            for methID in scoreTab:
                name = "m" + methID
                subjData[subjID][name] = scoreTab[methID]

        # write each subject's score to output file
        for subjID in batch.getSubIDOrder():
            
            sf.write(str(subjID))
            combineCSV.write(configInfo["SUBJFILELOC"].split('/')[1]+",")
            combineCSV.write(str(subjID))
            for name in score_names:
                sf.write(',' + str(subjData[subjID][name]))
                combineCSV.write(',' + str(subjData[subjID][name]))
            sf.write(','+responseId+','+eLeasMatchId+','+age+','+gender)#added on 9 November to include additional Info requested by Prof Lane. Code by Zain Islam
            sf.write('\n')
            combineCSV.write(','+responseId+','+eLeasMatchId+','+age+','+gender)#added on 25 November to write values in Combined CSV Code by Zain Islam
            combineCSV.write('\n')
            
    except IOError:
        print "Warning: Could not open " + fileLoc + " for score data CSV output."
    finally:
        sf.close()
        combineCSV.close()
