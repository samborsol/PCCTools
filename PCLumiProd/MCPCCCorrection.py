import sys,os
from math import exp
import argparse
import subprocess
import ROOT
import array

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--injection", default=26, type=int, help="The number of injections in the fill scheme")
parser.add_argument("-n", "--nbi", default=72, type=int, help="The number of bunches per injection")
parser.add_argument("-t", "--total", default=1740, type=int, help="The total number of active bunches")
parser.add_argument('-p', '--par', default="0.074,0.0,0.00086,0.014", help="The parameters for type1 and type2 correction (0.074,0.0,0.00086,0.014)")
parser.add_argument("-l", "--label", default="", help="The label for outputs")

args = parser.parse_args()



if args.par!="":
    pars=args.par.split(",")
    if len(pars) >= 3:
        a1=float(pars[0])
        a2=float(pars[1])
        b=float(pars[2])
        c=float(pars[3])

NActive = args.total
nbi = args.nbi
ninj = args.injection

BXLength=3564
SBIL=3
#can = ROOT.TCanvas("can", "can", 800, 800)
#can.cd()

type2CorrTemplate = ROOT.TH1F("type2CorrTemplate", "", BXLength, 0, BXLength)
for i in range(1, BXLength):
    type2CorrTemplate.SetBinContent(i, b*exp(-(i-2)*c))


h_corrected = ROOT.TH1F("h_corrected", "The Correct SBIL Histogram", BXLength, 0, BXLength)
h_recorded = ROOT.TH1F("h_recorded", "The Recorded SBIL Histogram", BXLength, 0, BXLength)
 

#number of trains in each group (4 groups in total)
nt=int((ninj-1)/4)
res = ninj-1-nt*4

#Calculate the distance between 4 groups 
Z=NActive+37*(ninj-4-1)
dist = int((BXLength-Z)/4)

#Calculate the number of bunches in the leading train
nlead = NActive-nbi*(ninj-2)

train_group=[0,0,0,0]
train_group[0]=nt-1
train_group[1]=nt
train_group[2]=nt
train_group[3]=nt

if res!=0:
    if res==1:
        train_group[3]+=1
    elif res==2:
        train_group[3]+=1
        train_group[2]+=1
    
    elif res==3:
        train_group[3]+=1
        train_group[2]+=1
        train_group[1]+=1


for ibx in range(1, nlead+1):
    h_corrected.SetBinContent(ibx, SBIL)

curr_bin = nlead+1
for i in range(4):
    for i_0 in range(train_group[i]):
        for i_n in range(37):
            h_corrected.SetBinContent(curr_bin, 0)
            curr_bin+=1
        for i_a in range(nbi):
            h_corrected.SetBinContent(curr_bin, SBIL)
            curr_bin+=1
    for i_d in range(dist):
        h_corrected.SetBinContent(curr_bin,0)
        curr_bin+=1

h_recorded = h_corrected.Clone()

for ibx in range(1, BXLength):
    for jbx in range(ibx+1, BXLength):
        if jbx==ibx+1:
            h_recorded.SetBinContent(jbx, h_recorded.GetBinContent(jbx)+h_corrected.GetBinContent(ibx)*type2CorrTemplate.GetBinContent(jbx-ibx)+h_recorded.GetBinContent(ibx)*a1)
        else:
            h_recorded.SetBinContent(jbx, h_recorded.GetBinContent(jbx)+h_corrected.GetBinContent(ibx)*type2CorrTemplate.GetBinContent(jbx-ibx))

lumi_corr = 0
lumi_record = 0

for ibx in range(1, BXLength):
    if h_recorded.GetBinContent(ibx)>0.5:
        lumi_corr+=h_corrected.GetBinContent(ibx)
        lumi_record+=h_recorded.GetBinContent(ibx)



print "The Overall Correction Factor is: ", lumi_corr/lumi_record
#h_recorded.Draw("HIST")
#can.SaveAs("test.png")
