import ROOT
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="", help="The csv file containing the corrections fill by fill")
parser.add_argument("-l", "--label", default="Correctio_Factor_PCC_Run2016", help="The label for output file")

args = parser.parse_args()

filename = args.file
corrfile = open(filename)

corrPerFill = {}

for line in corrfile.readlines():
    items=line.split(",")
    try:
        fill=int(items[0])
        corr=float(items[1])
        
        corrPerFill[fill]=corr
    except:
        print "Problem with line", line

can = ROOT.TCanvas("can", "", 1000, 700)
can.cd()
can.SetTickx()
can.SetTicky()


iFill = 0
gra_corr = ROOT.TGraph()
for Fill in corrPerFill.keys():
    gra_corr.SetPoint(iFill, Fill, corrPerFill[Fill])
    iFill+=1

gra_corr.SetTitle("; Fill; Correction Factor")
gra_corr.GetYaxis().SetTitleOffset(1.0)
gra_corr.SetMarkerStyle(23)
gra_corr.SetMarkerSize(1)
gra_corr.SetMarkerColor(ROOT.kBlue)
gra_corr.Draw("AP")

text=ROOT.TLatex(0.72,0.92,"2016  (13TeV)")
text.SetNDC()
text.SetTextFont(62)
text.SetTextSize(0.05)
text2=ROOT.TLatex(0.15,0.92,"CMS #bf{#scale[0.75]{#it{Preliminary}}}")
text2.SetNDC()
text2.SetTextSize(0.05)
text2.SetTextFont(62)

text.Draw("SAME")
text2.Draw("SAME")

can.SaveAs(args.label+".png")
can.SaveAs(args.label+".C")


