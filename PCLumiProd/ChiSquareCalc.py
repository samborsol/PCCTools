import sys, os
from math import exp
import argparse
import subprocess
from array import array

import ROOT
from ROOT import TGraph2D

parser=argparse.ArgumentParser()

parser.add_argument("-p", "--path", default="", help="The path to the output correciton files")
parser.add_argument("-n", "--name", default="After_Corr", help="The name of histogram that need to be checked")
parser.add_argument("-r", "--run", default="", help="The run number to be checked")
parser.add_argument("-l", "--label", default="", help="The label for outputs")
parser.add_argument("-b", "--batch", action='store_true', default=False, help="Batch mode (doesn't make GUI TCanvases)")
parser.add_argument("-c", "--cut", default="100", help="The number of bins cut for the long tail after a bunch train when calulating the Chi2s")

args=parser.parse_args()

ROOT.gStyle.SetOptStat(0)
if args.batch is True:
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

histname= args.name
run_num = args.run
cut_value = int(args.cut)

a_array = array('d')
b_array = array('d')
c_array = array('d')

chi2overall_array = array('d')
chi2train_array = array('d')
chi2tail_array = array('d')
chi2combine_array = array('d')

outfile=ROOT.TFile("Grid_Chi2_"+args.run+"_"+args.cut+"_"+args.label+".root", "recreate")

files=os.listdir(args.path)
files.sort()
for filename in files:
    tfile=ROOT.TFile(args.path+"/"+filename)
    histpar_a = tfile.Get("Parameter_a")
    histpar_b = tfile.Get("Parameter_b")
    histpar_c = tfile.Get("Parameter_c")

    a = histpar_a.GetBinContent(4)
    b = histpar_b.GetBinContent(4)
    c = histpar_c.GetBinContent(4)

    hist_tocheck = tfile.Get(histname+"_"+run_num)

    maxi=hist_tocheck.GetMaximum()

    nonlumi_list=[]
    dist_list=[]   # The distance between the nonlumi BX and the closest active BX before it
    flag_train_list=[] # Whether the nonlumi BX is within a Bunch train

    first_actBX=False  # Whether the BX is behind the first active BX
    dist=-1

    for i in range(hist_tocheck.GetNbinsX()):

        if not first_actBX:
            if hist_tocheck.GetBinContent(i)>0.2*maxi:
                dist=0
                first_actBX=True
            continue

        if hist_tocheck.GetBinContent(i)>0.2*maxi:
            dist=0
        else:
            dist+=1
            nonlumi_list.append(i)
            dist_list.append(dist)

            if dist==1 and hist_tocheck.GetBinContent(i+1)>0.2*maxi:
                flag_train_list.append(True)
            else:
                flag_train_list.append(False)


    Chi2_Overall=0 # The Chi2 based on all the non-lumi BXs
    Chi2_Train=0 # The Chi2 only based on the non-lumi BXs within a bunch train
    Chi2_Tail=0 # The Chi2 only based on the long tail after a bunch train (with the Bin number cut)
    Chi2_combine=0 # The Chi2 based on both the non-lumi BXs within bunch trains and the long tail after bunch trains

    for j in range(len(nonlumi_list)):
        Chi2_Overall+=hist_tocheck.GetBinContent(nonlumi_list[j])*hist_tocheck.GetBinContent(nonlumi_list[j])
        if flag_train_list[j]:
            Chi2_Train+=hist_tocheck.GetBinContent(nonlumi_list[j])*hist_tocheck.GetBinContent(nonlumi_list[j])
        elif dist_list[j]<cut_value:
            Chi2_Tail+=hist_tocheck.GetBinContent(nonlumi_list[j])*hist_tocheck.GetBinContent(nonlumi_list[j])

        if dist_list[j]<cut_value:
            Chi2_combine+=hist_tocheck.GetBinContent(nonlumi_list[j])*hist_tocheck.GetBinContent(nonlumi_list[j])

    print "Parameter a: ", a
    print "Parameter b: ", b
    print "Parameter c: ", c
    print "Chi2_Overall: ", Chi2_Overall
    print "Chi2_Train: ", Chi2_Train
    print "Chi2_Tail: ", Chi2_Tail
    print "Chi2_combine: ", Chi2_combine

    a_array.append(a)
    b_array.append(b)
    c_array.append(c)

    chi2overall_array.append(Chi2_Overall)
    chi2train_array.append(Chi2_Train)
    chi2tail_array.append(Chi2_Tail)
    chi2combine_array.append(Chi2_combine)


grchi2overall = TGraph2D(len(b_array), b_array, c_array, chi2overall_array)
grchi2overall.GetXaxis().SetTitle("b")
grchi2overall.GetYaxis().SetTitle("c")

grchi2train = TGraph2D(len(b_array), b_array, c_array, chi2train_array)
grchi2train.GetXaxis().SetTitle("b")
grchi2train.GetYaxis().SetTitle("c")

grchi2tail = TGraph2D(len(b_array), b_array, c_array, chi2tail_array)
grchi2tail.GetXaxis().SetTitle("b")
grchi2tail.GetYaxis().SetTitle("c")

grchi2combine = TGraph2D(len(b_array), b_array, c_array, chi2combine_array)
grchi2combine.GetXaxis().SetTitle("b")
grchi2combine.GetYaxis().SetTitle("c")

outfile.WriteTObject(grchi2overall, "grchi2overall")
outfile.WriteTObject(grchi2train, "grchi2train")
outfile.WriteTObject(grchi2tail, "grchi2tail")
outfile.WriteTObject(grchi2combine, "grchi2combine")
outfile.Close()


