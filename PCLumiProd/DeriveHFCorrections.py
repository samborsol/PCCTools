import sys, os
from math import exp
import argparse
import subprocess
import ROOT

parser=argparse.ArgumentParser()
#parser.add_argument("-h", "--help", help="Display this message.")
parser.add_argument("-f", "--file", default="", help="The path to a cert tree.")
parser.add_argument("-d", "--dir",  default="", help="The path to a directory of cert trees.")
parser.add_argument("-r", "--runs", default="", help="Comma separated list of runs.")
parser.add_argument("--auto", default=False, action="store_true", help="Determine the runs from the certtree")
parser.add_argument("-l", "--label", default="", help="The label for outputs")
parser.add_argument('-b', '--batch',   action='store_true', default=False, help="Batch mode (doesn't make GUI TCanvases)")

args=parser.parse_args()

def findRange( hist, cut):
    gaplist=[]
    for i in range(1,3600):
        if hist.GetBinContent(i)<cut:
            gaplist.append(i)
    return gaplist

ROOT.gStyle.SetOptStat(0)
if args.batch is True:
    ROOT.gROOT.SetBatch(ROOT.kTRUE)


corrTemplate=ROOT.TH1F("corrTemplate","",3600,0,3600)

#corrTemplate.SetBinContent(1,a+b*exp(c))
#for i in range(1,3600):
#    corrTemplate.SetBinContent(i,b*exp(-(i-2)*c))
#corrTemplate.GetXaxis().SetRangeUser(0,100)

filename=args.file
if args.runs!="":
    runs=args.runs.split(",")
else:
    runs=[]
label=args.label


templatefile=ROOT.TFile("HF_template.root")
h_template = templatefile.Get("h_template")
corrTemplate = h_template.Clone()

newfile=ROOT.TFile("Overall_Correction_"+label+".root", "recreate")

tfile=ROOT.TFile(filename)
tree=tfile.Get("certtree")

tree.SetBranchStatus("*",0)
tree.SetBranchStatus("run*", 1)

if args.auto:
    nentries=tree.GetEntries()

    for iev in range(nentries):
        tree.GetEntry(iev)
        if str(tree.run) not in runs:
            print "Adding",tree.run
            runs.append(str(tree.run))

    print "auto", runs
    runs.sort()

tree.SetBranchStatus("fill*", 1)
tree.SetBranchStatus("LS*", 1)
tree.SetBranchStatus("HFLumi_perBX*", 1)
tree.SetBranchStatus("HFBXid*",1)
tree.SetBranchStatus("nBXHF*", 1)

for run in runs:
    runnum=int(run)

    histnoise=ROOT.TH1F("histnoise","",3600,0,3600)
    histfull=ROOT.TH1F("histfull","",3600,0,3600)
    normfull=ROOT.TH1F("normfull","",3600,0,3600)
    corrfill=ROOT.TH1F("corrfill","",3600,0,3600)

    nentries=tree.GetEntries()

    for iev in range(nentries):
        tree.GetEntry(iev)
        if tree.LS<3700 and tree.run==runnum:
            for ibx in range(tree.nBXHF):
                histfull.Fill(tree.HFBXid[ibx], tree.HFLumi_perBX[ibx])
                normfull.Fill(tree.HFBXid[ibx], 1)

    histfull.Divide(normfull)
    histsig=histfull.Clone()
    histfull.SetTitle("Random Triggers in Run "+run+";BX;Average PCC SBIL Hz/ub")
    histsig.SetTitle("Random Triggers in Run "+run+", after correction;BX; Average PCC SBIL Hz/ub")
    histfull.SetLineColor(416)
    histfull.GetXaxis().SetRangeUser(0,2000)
    histfull.GetYaxis().SetRangeUser(-0.02,3.0)

    can=ROOT.TCanvas("can_corr_temp","",800,800)
    canfull=ROOT.TCanvas("can_full","",800,800)
    cansig=ROOT.TCanvas("can_sig","",800,800)
    canfill=ROOT.TCanvas("can_fill","",800,800)
    canratio=ROOT.TCanvas("ratio_fill","",800,800)

    can.cd()
    corrTemplate.SetTitle("Correction Function Template")
    corrTemplate.Draw("HIST")
    can.SaveAs("SBIL_randoms_"+run+"_corrTemplate_"+label+".png")

    canfull.cd()
    histfull.Draw()
    canfull.SaveAs("full_SBIL_randoms_"+run+"_full_"+label+".png")


    cansig.cd()
    noise=0



    
    gap=False
    idl=0
    num_cut=20
    for l in range(1, num_cut+1):
        noise+=histsig.GetBinContent(l)
        idl+=1
   
    noise=noise/num_cut     

    hist_afterTypeI=histsig.Clone()


    for i in range(1,3565):
        for j in range(i+1,i+3565):
            binsig_i=histsig.GetBinContent(i)
            binfull_i=histfull.GetBinContent(i)
            if j<=3564:
                histsig.SetBinContent(j,histsig.GetBinContent(j)-binsig_i*corrTemplate.GetBinContent(j-i))
                corrfill.SetBinContent(j, corrfill.GetBinContent(j)+binsig_i*corrTemplate.GetBinContent(j-i))
            else:
                #print j-3564
                histsig.SetBinContent(j-3564,histsig.GetBinContent(j-3564)-binsig_i*corrTemplate.GetBinContent(j-i))
                corrfill.SetBinContent(j-3564, corrfill.GetBinContent(j-3564)+binsig_i*corrTemplate.GetBinContent(j-i))


    histsig.GetXaxis().SetRangeUser(0,2000)
    histsig.GetYaxis().SetRangeUser(-0.03,3.0)
    histsig.Draw()
    cansig.SaveAs("full_SBIL_randoms_"+run+"_signal"+label+".png")

    canfill.cd()
    corrfill.SetTitle("The Overall Correction in the Run "+run)
    corrfill.Draw()
    canfill.SaveAs("full_SBIL_randoms_"+run+"_fill_"+label+".png")

    ratiocorr=corrfill.Clone()
    ratiocorr.Divide(histfull)

    canratio.cd()
    ratiocorr.SetTitle("The Ratio of Overall Correction in the Run "+run)
    ratiocorr.GetXaxis().SetTitle("BX")
    ratiocorr.GetYaxis().SetTitle("Ratio")
    ratiocorr.Draw()
    canratio.SaveAs("full_SBIL_randoms_"+run+"_ratio_"+label+".png")

    ratio_gap=ROOT.TH1F("ratio_gap", "",100,0,2.8)
    checklist=findRange(histfull, 0.2)
    for l in checklist:
        ratio_gap.Fill(ratiocorr.GetBinContent(l))

    ratio_noise=histnoise.Clone()
    ratio_noise.Divide(corrfill)

    newfile.WriteTObject(histfull,  "Before_Corr_"+run)
    newfile.WriteTObject(hist_afterTypeI, "After_TypeI_Corr_"+run)
    newfile.WriteTObject(histsig, "After_Corr_"+run)
    newfile.WriteTObject(histnoise, "Noise_"+run)
    newfile.WriteTObject(corrfill, "Overall_Correction_"+run)
    newfile.WriteTObject(ratiocorr, "Ratio_Correction_"+run)
    newfile.WriteTObject(ratio_gap, "Ratio_Nonlumi_"+run)
    newfile.WriteTObject(ratio_noise, "Ratio_Noise_"+run)
