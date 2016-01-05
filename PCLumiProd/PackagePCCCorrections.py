import sys, os
from math import exp
import subprocess
import ROOT
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The path to the corrections file.")
parser.add_argument("-r", "--runs", default="", help="Comma separated list of runs.")
parser.add_argument("-l", "--label", default="", help="Label for output file")
parser.add_argument("-a", "--auto", default=False, action='store_true', help="Find list of runs from the histograms in the file.")
args=parser.parse_args()


tfile=ROOT.TFile(args.file)
if args.runs!="":
    runs=args.runs.split(",")
else:
    runs=[]

lumiBlocks=[]

if args.auto:
    listFromFile=tfile.GetListOfKeys()
    lumiBlocks=[]
    #print "size",listFromFile.GetSize()
    for iList in range(listFromFile.GetSize()):
    #    print iList,listFromFile.At(iList).GetName()
        thisName=listFromFile.At(iList).GetName()
        if thisName.find("Overall_Correction")!=-1:
            lumiBlockText=thisName.split("Overall_Correction_")[1]
            if args.runs!="":
                thisRun=thisName.split("_")[2]
                if thisRun not in runs:
                    continue
            lumiBlocks.append(lumiBlockText)
            #print thisName,lumiBlockText
#print lumiBlocks

corrections={}
for lumiBlockText in lumiBlocks:
    #print lumiBlockText
    h_origin=tfile.Get("Before_Corr_"+lumiBlockText)
    h_after=tfile.Get("After_Corr_"+lumiBlockText)
    
    total_origin=0
    total_after=0
    for i in range(3600):
        if h_origin.GetBinContent(i) > 0.5:
            total_origin+=h_origin.GetBinContent(i)
            total_after+=h_after.GetBinContent(i)
    
    if total_origin>0:
        parts=lumiBlockText.split("_")
        run=int(parts[0])
        LS1=int(parts[1].split("LS")[1])
        LSN=int(parts[2].split("LS")[1])
        corrections[(run,LS1,LSN)]=total_after/total_origin 

corrPCCFile=open("corrPCC"+args.label+".csv", "a+")
corrRuns=corrections.keys()
corrRuns.sort()

for run,LS1,LSN in corrRuns:
    try:
        corrPCCFile.write(str(run)+","+str(LS1)+","+str(LSN)+",")
        corrPCCFile.write("{:.4f}".format(float(corrections[(run,LS1,LSN)]))+"\n")
    except:
        print "can't fill for",
        try:
            print run,LS1,LSN,
            print corrections[(run,LS1,LSN)]
        except:
            print "I can't print"
corrPCCFile.close()
