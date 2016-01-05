import sys, os
import argparse
import ROOT
from ROOT import TFile, TCanvas, TH1F
from ROOT import gStyle
from ROOT import kGreen, kRed, kBlue

parser=argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The Correction File")
parser.add_argument("-r", "--run", help="The run number to be checked")
parser.add_argument("-l", "--label", help="The label for outputs")

args = parser.parse_args()

filename=args.file
run=args.run

tfile=TFile(filename)

h_before=tfile.Get("Before_Corr_"+run)
h_after_typeI=tfile.Get("After_TypeI_Corr_"+run)
h_after=tfile.Get("After_Corr_"+run)

can=TCanvas("can","",800,800)

can.cd()

can.SetTickx()
can.SetTicky()

h_before.SetLineColor(kGreen)
h_before.SetTitle("Random Triggers in Run "+run)
h_before.GetYaxis().SetRangeUser(-0.035,0.25)
h_before.GetYaxis().SetTitleOffset(1.4)

h_before.Draw()

h_after_typeI.SetLineColor(kBlue)
h_after_typeI.Draw("SAME")

h_after.SetLineColor(kRed)
h_after.Draw("SAME")

can.SaveAs("plot_"+args.label+"_"+run+".eps")

