import sys, os
from math import exp
ROOTSYS='/Users/jingyuluo/Downloads/Program/root/lib'

sys.path.append(ROOTSYS)
import ROOT
from ROOT import TFile

def findRange( hist, cut):
    gaplist=[]
    for i in range(1,3600):
        if hist.GetBinContent(i)<cut:
            gaplist.append(i)
    return gaplist


def calculate_Chi2(hist, rangelist, a, b, c):
    #corrtemp=ROOT.TH1F("corrtemp", 300,0,300)
    corrtemp=ROOT.TH1F("corrtemp","",300,0,300)
    corrtemp.SetBinContent(1,a)
    print a,b,c
    for i in range(2,300):
        corrtemp.SetBinContent(i, b*exp(-(i-2)*c))
    noise=0
    for m in range(2,36):
        noise=noise+hist.GetBinContent(m)
    noise=noise/34

    histsig=hist.Clone()
    for l in range(1,3600):
        histsig.SetBinContent(l, histsig.GetBinContent(l)-noise)
    for i in range(1,3600):
        if i<3299:
            for j in range(i+1,i+300):
                bin_i = histsig.GetBinContent(i)
                histsig.SetBinContent(j, histsig.GetBinContent(j)-bin_i*corrtemp.GetBinContent(j-i))
        else:
            for j in range(i+1,3600):
                bin_i = histsig.GetBinContent(i)
                histsig.SetBinContent(j, histsig.GetBinContent(j)-bin_i*corrtemp.GetBinContent(j-i))
    Chi2=0
    for k in rangelist:
        if hist.GetBinContent(k)>1.2:
            Chi2=Chi2+160*histsig.GetBinContent(k)*histsig.GetBinContent(k)
        else:
            Chi2=Chi2+histsig.GetBinContent(k)*histsig.GetBinContent(k)
    return Chi2


def Iteration_min(histfull, rangelist,a, b, c, length, step, idx):
    print "the {0}th step!".format(idx)
    idx=idx+1
    Chi2_0=calculate_Chi2(histfull, rangelist, a, b, c)
    min_i=0
    min_j=0
    min_Chi2=Chi2_0
    for i in range(-1, 2):
        for j in range(-1, 2):
            Chi2_ij=calculate_Chi2(histfull, rangelist, a, b+i*length, c+j*length)
            if (Chi2_ij<min_Chi2):
                min_i=i
                min_j=j
                min_Chi2=Chi2_ij
    print a,b+min_i*length, c+min_j*length, min_Chi2
    if idx<step:
        if min_i==0 and min_j==0:
            Iteration_min(histfull, rangelist, a, b, c, length/2, step, idx)
        else:
            Iteration_min(histfull, rangelist, a, b+min_i*length, c+min_j*length, length, step, idx)
    else:
         return a, b+length*min_i, c+length*min_j, min_Chi2


filename=sys.argv[1]
run=sys.argv[2]
tfile=ROOT.TFile(filename)
tree=tfile.Get("certtree")

histfull=ROOT.TH1F("histfull","",3600,0,3600)
normfull=ROOT.TH1F("normfull","",3600,0,3600)

tree.Draw("PCBXid>>histfull", "PC_lumi_B3p8_perBX")
tree.Draw("PCBXid>>normfull")
histfull.Divide(normfull)

checklist=findRange(histfull, 0.2)
Chis= calculate_Chi2(histfull, checklist, 0.06, 0.006, 0.008)
print Chis
print Iteration_min(histfull, checklist,0.073827,0.0008125,0.011407, 0.0005,100,0)
