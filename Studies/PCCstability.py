import ROOT
from ROOT import TH1F
import sys,os
import numpy
import math
import argparse
import pickle
import time
import json

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('-c','--certfile', type=str, default="", help='The certfile to input')
parser.add_argument('-o','--output',type=str, default="", help='The path for the output file')
parser.add_argument('-j','--json', type=str, default="", help='JSON file of run/LSs to filter')
parser.add_argument('-l','--label', type=str, default="", help='The label of output file')

args=parser.parse_args()

if args.output!="":
    outpath=args.output

    if outpath.find("/store")==0:
        outpath="root://eoscms//eos/cms"+outpath
    newfilename="PCC_ratio_"+args.label+".root"
    newfile=ROOT.TFile.Open(newfilename, "recreate")


#hist_PCCratio_Layer = {}
hist_PCC_layer = {}

for iLayer in range(5):
    #hist_PCCratio_Layer[iLayer] = TH1F("h_PCCratio_Layer_"+str(iLayer), "h_PCCratio_Layer_"+str(iLayer), 10000, 0, 10000)
    #hist_PCCratio_Layer[iLayer].Sumw2()

    hist_PCC_layer[iLayer] = TH1F("h_PCC_Layer_"+str(iLayer), "h_PCC_Layer_"+str(iLayer), 800, 1436000000, 1437000000)
    #hist_PCC_layer[iLayer].Sumw2()
hist_PCC_total = TH1F("h_PCC_total", "h_PCC_total", 800, 1436000000, 1437000000)
hist_PCC_nLS = TH1F("h_PCC_nLS", "h_PCC_nLS", 800, 1436000000, 1437000000)

runLSData = json.load(open(args.json))


def ISRunLSInList(run, LS):
    if not runLSData.has_key(str(run)):
        return False

    else:
        for LSRange in runLSData[str(run)]:
            if int(LSRange[0])<=LS and int(LSRange[1])>=LS:
                return True 

if args.certfile!="":
    filename=args.certfile

    if filename.find("/store")==0:
        filename="root://eoscms//eos/cms"+filename

    tfile=ROOT.TFile.Open(filename)
    
    tree=tfile.Get("certtree")
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("run*", 1)
    tree.SetBranchStatus("LS*", 1)
    tree.SetBranchStatus("timeStamp*", 1)
    tree.SetBranchStatus("nCluster*", 1)
    tree.SetBranchStatus("nPCPerLayer*", 1)

    nentries = tree.GetEntries()
   
    for iev in range(nentries):

        tree.GetEntry(iev)
        if iev%1==0:
            print "iev,", iev
            
        if ISRunLSInList(tree.run, tree.LS):
            print "yes!"
            print tree.timeStamp
           # if hist_PCC_nLS.GetBinContent(hist_PCC_nLS.FindBin(tree.run))<50:
            hist_PCC_total.Fill(tree.timeStamp, tree.nCluster)
            hist_PCC_nLS.Fill(tree.timeStamp, 1)

            for iLayer in range(5):
                hist_PCC_layer[iLayer].Fill(tree.timeStamp, tree.nPCPerLayer[iLayer])    

if args.output!="":
    #newfile.WriteTObject(
    newfile.Write()
    newfile.Close()
            
        
    
   
