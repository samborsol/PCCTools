import sys, os
from math import exp
import argparse
import subprocess
import ROOT
import array

parser=argparse.ArgumentParser()
#parser.add_argument("-h", "--help", help="Display this message.")
parser.add_argument("-f", "--onefile", default="", help="The path to a cert tree or root file with \"Before\" histograms.")
parser.add_argument("-d", "--dir",  default="", help="The path to a directory of cert trees or roots file with \"Before\" histograms.")
parser.add_argument("-r", "--runs", default="", help="Comma separated list of runs.")
parser.add_argument("--auto", default=False, action="store_true", help="Determine the runs from the certtree")
parser.add_argument("-l", "--label", default="", help="The label for outputs")
parser.add_argument("-a", "--all", default=True, help="Apply both the type1 and type2 correction")
parser.add_argument("--quadTrainCorr", default=0.00, help="Apply a quadratic correction to in-train BXs (Default:  0.02 ub/Hz)")
parser.add_argument("--noType1", action='store_true', default=False, help="Only apply the type2 correction")
parser.add_argument("--noType2", action='store_true', default=False, help="Only apply the type1 correction")
parser.add_argument("-u","--useresponse", action='store_true', default=False, help="Use the final response instead of the real activity to calculate the Type2 Correction")
parser.add_argument('-b', '--batch',   action='store_true', default=False, help="Batch mode (doesn't make GUI TCanvases)")
parser.add_argument('-p', '--par', default="0.074,0.0,0.00086,0.014", help="The parameters for type1 and type2 correction (0.059,0.0,0.0007,0.013)")
parser.add_argument('--filterByRunInFileName', default=False, action='store_true', help="Filter by run in the name of the files.")
parser.add_argument('--nLSInLumiBlock', default=500, type=int, help="Number of LSs to group for evaluation (Default:  500)")
parser.add_argument('--buildFromScratch', default=1, type=int, help="Start from cert trees (default); do --buildFromScratch=0 to start from \"Before\" histograms")

args=parser.parse_args()

BXLength=3600
zeroes=array.array('d',[0.]*BXLength)
def findRange( hist, cut):
    gaplist=[]
    for i in range(1,BXLength):
        if hist.GetBinContent(i)<cut:
            gaplist.append(i)
    return gaplist

ROOT.gStyle.SetOptStat(0)
if args.batch is True:
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

a1=0.0#0.06636#0.073827#0.078625#0.076825
a2=0.0
b=0.0#0.00083#0.00078#0.00067#0.00083#0.000811#0.0007891#0.00080518#0.00080518#0.0008125#0.00090625#0.00047
c=0.0#0.0126#0.012#0.017#0.0126#0.012282#0.011867#0.01261#0.0098

b2=0.0
c2=0.0

if args.par!="":
    pars=args.par.split(",")
    if len(pars) >= 3:
        a1=float(pars[0])
        a2=float(pars[1])
        b=float(pars[2])
        c=float(pars[3])
    if len(pars) >= 5:
        b2=float(pars[4])
        c2=float(pars[5])

if args.noType1:
    a1=0
    a2=0
if args.noType2:
    b=0
    b2=0

# Print out the paramters for correction:
print "parameter a1: ", a1
print "parameter a2: ", a2
print "parameter b: ", b
print "parameter c: ", c
print "parameter b2: ", b2
print "parameter c2: ", c2


histpar_a1=ROOT.TH1F("histpar_a1","",10, 0, 10)
histpar_a2=ROOT.TH1F("histpar_a2","",10, 0, 10)

histpar_b=ROOT.TH1F("histpar_b","",10, 0, 10)
histpar_c=ROOT.TH1F("histpar_c","",10, 0, 10)

histpar_b2=ROOT.TH1F("histpar_b2","",10, 0, 10)
histpar_c2=ROOT.TH1F("histpar_c2","",10, 0, 10)

histpar_quad=ROOT.TH1F("histpar_quad","",10, 0, 10)
args.quadTrainCorr=float(args.quadTrainCorr)

for ia1 in range(10):
    histpar_a1.SetBinContent(ia1,a1)
for ia2 in range(10):
    histpar_a2.SetBinContent(ia2,a2)
for ib in range(10):
    histpar_b.SetBinContent(ib,b)
for ic in range(10):
    histpar_c.SetBinContent(ic,c)
for ib2 in range(10):
    histpar_b2.SetBinContent(ib2,b2)
for ic2 in range(10):
    histpar_c2.SetBinContent(ic2,c2)
for iq in range(10):
    histpar_quad.SetBinContent(iq,args.quadTrainCorr)

type2CorrTemplate=ROOT.TH1F("type2CorrTemplate","",BXLength,0,BXLength)

# type 2 model is simple exponential
for i in range(1,BXLength):
    type2CorrTemplate.SetBinContent(i,b*exp(-(i-2)*c)+b2*exp(-(i-2)*c2))
type2CorrTemplate.GetXaxis().SetRangeUser(0,100)

fixRuns=False
if args.runs!="":
    runs=args.runs.split(",")
    fixRuns=True
else:
    runs=[]
label=args.label

newfile=ROOT.TFile("Overall_Correction_"+label+".root", "recreate")
newfile.WriteTObject(histpar_a1, "Parameter_a1")
newfile.WriteTObject(histpar_a2, "Parameter_a2")
newfile.WriteTObject(histpar_b, "Parameter_b")
newfile.WriteTObject(histpar_c, "Parameter_c")
newfile.WriteTObject(histpar_b2, "Parameter_b2")
newfile.WriteTObject(histpar_c2, "Parameter_c2")
newfile.WriteTObject(histpar_quad, "Parameter_quad")
maxLSInRun={}

filenames=[]
if args.onefile!="":
    filenames.append(args.onefile)

if args.dir!="":
    if args.dir.find("/store")==0:
        eosfilenames=subprocess.check_output(["/afs/cern.ch/project/eos/installation/0.3.4/bin/eos.select","ls", args.dir])
        eosfilenames=eosfilenames.split("\n")
        for filename in eosfilenames:
            if filename is not "" and filename.find(".root")!=-1:
                filenames.append("root://eoscms//eos/cms"+args.dir+"/"+filename)
    else:
        shortFileNames=os.listdir(args.dir)
        for shortFileName in shortFileNames:
            if shortFileName.find(".root")!=-1:
                filenames.append(args.dir+"/"+shortFileName)


if args.filterByRunInFileName:
    if not fixRuns:
        print "You have not fixed the runs, but are trying to filter."
        print "You would not select anything, so the program is exiting."
        sys.exit(-1)
    print "before",len(filenames)
    foundFiles=[]
    for filename in filenames:
        foundRun=False
        for run in runs:
            if filename.find(run) != -1:
                #print run,"found in",filename
                foundRun=True
        if foundRun:
            foundFiles.append(filename)
        
    filenames=foundFiles
    print "after",len(filenames)

if args.buildFromScratch==1:
    for filename in filenames:
        tfile=ROOT.TFile.Open(filename)
        tree=tfile.Get("certtree")
        
        tree.SetBranchStatus("*",0)
        tree.SetBranchStatus("run*", 1)
        tree.SetBranchStatus("LS*", 1)
        
        nentries=tree.GetEntries()
        
        for iev in range(nentries):
            tree.GetEntry(iev)
            if str(tree.run) not in runs and not fixRuns:
                print "Adding",tree.run
                runs.append(str(tree.run))
            if not maxLSInRun.has_key(str(tree.run)):
                maxLSInRun[str(tree.run)]=tree.LS
            elif maxLSInRun[str(tree.run)]<tree.LS:
                maxLSInRun[str(tree.run)]=tree.LS
                
        tfile.Close()

    for run in maxLSInRun.keys():
        print run,maxLSInRun[run]

print "runs", runs

runs.sort()

noisePerBX={}
allLumiPerBX={}
normPerBX={}
corrPerBX={}

allCorrLumiPerBX={}
allLumiType1CorrPerBX={}
allLumiType1And2CorrPerBX={}

corrRatioPerBX={}
noiseToCorrRatio={}
Fill={}
LBKeys=[]


# read events from data cert trees
if args.buildFromScratch==1:
    for run in runs:
        runnum=int(run)
    
        for iLB in range(maxLSInRun[run]/args.nLSInLumiBlock+1):
            LBKey=run+"_LS"+str(iLB*args.nLSInLumiBlock+1)+"_LS"+str((iLB+1)*args.nLSInLumiBlock)
    
            noisePerBX[LBKey]=ROOT.TH1F("noisePerBX"+LBKey,"",BXLength,0,BXLength)
            allLumiPerBX[LBKey]=ROOT.TH1F("allLumiPerBX"+LBKey,"",BXLength,0,BXLength)
            normPerBX[LBKey]=ROOT.TH1F("normPerBX"+LBKey,"",BXLength,0,BXLength)
            corrPerBX[LBKey]=ROOT.TH1F("corrPerBX"+LBKey,"",BXLength,0,BXLength)

            LBKeys.append(LBKey)
        
    iFile=0
    
    for filename in filenames:
        tfile=ROOT.TFile.Open(filename)
        tree=tfile.Get("certtree")
        
        tree.SetBranchStatus("*",0)
        tree.SetBranchStatus("run*", 1)
        tree.SetBranchStatus("fill*", 1)
        tree.SetBranchStatus("LS*", 1)
        tree.SetBranchStatus("PC_lumi_B3p8_perBX*", 1)
        tree.SetBranchStatus("PCBXid*",1)
        
        nentries=tree.GetEntries()
       
        for iev in range(nentries):
            if iev%1000==101:
                print "event",iev
            tree.GetEntry(iev)
            if str(tree.run) not in runs:
                continue
            iLB=(tree.LS-1)/args.nLSInLumiBlock
            LBKey=str(tree.run)+"_LS"+str(iLB*args.nLSInLumiBlock+1)+"_LS"+str((iLB+1)*args.nLSInLumiBlock)
            Fill[LBKey]=str(tree.fill)
            #print tree.run,tree.LS,iLB,LBKey
            for ibx in range(tree.nBX):
                try:
                    allLumiPerBX[LBKey].Fill(tree.PCBXid[ibx], tree.PC_lumi_B3p8_perBX[ibx])
                    normPerBX[LBKey].Fill(tree.PCBXid[ibx], 1)
                except:
                    print "problem filling allLumiPerBX or normPerBX"
                    print tree.fill,tree.run,tree.LS,iLB,LBKey
    
        tfile.Close()
    
        iFile=iFile+1
        print "iFile",iFile

# instead of reading events from data cert trees
# take "Before_Corr_" histograms from previously made corrections
# and apply a new suite of corrections.
else:
    for filename in filenames:
        tfile=ROOT.TFile.Open(filename)
        tKeys=tfile.GetListOfKeys()
        for tKey in tKeys:
            thisName=tKey.GetName()
            if thisName.find("Before_Corr_")==0:
                LBKey=thisName.split("efore_Corr_")[1]
                if LBKey in LBKeys:
                    print "This shouldn't happen... I already found these corrections... skipping."
                    continue
                
                LBKeys.append(LBKey)
                
                allLumiPerBX[LBKey]=tfile.Get("Before_Corr_"+LBKey)
                #allLumiPerBX[LBKey]=ROOT.TH1F("allLumiPerBX"+LBKey,"",BXLength,0,BXLength)
                noisePerBX[LBKey]=ROOT.TH1F("noisePerBX"+LBKey,"",BXLength,0,BXLength)
                corrPerBX[LBKey]=ROOT.TH1F("corrPerBX"+LBKey,"",BXLength,0,BXLength)

        #tfile.Close()

print LBKeys

#for run in runs:
#    runnum=int(run)
#
#    for iLB in range(maxLSInRun[run]/args.nLSInLumiBlock+1):
#        LBKey=run+"_LS"+str(iLB*args.nLSInLumiBlock+1)+"_LS"+str((iLB+1)*args.nLSInLumiBlock)


for LBKey in LBKeys:
    run=LBKey.split("_")[0]
    if args.buildFromScratch==1:
        allLumiPerBX[LBKey].Divide(normPerBX[LBKey])
    allLumiPerBX[LBKey].SetError(zeroes)
    allCorrLumiPerBX[LBKey]=allLumiPerBX[LBKey].Clone()
    allLumiPerBX[LBKey].SetTitle("Random Triggers in Run "+run+";BX;Average PCC SBIL Hz/ub")
    allCorrLumiPerBX[LBKey].SetTitle("Random Triggers in Run "+run+", after correction;BX; Average PCC SBIL Hz/ub")
    allLumiPerBX[LBKey].SetLineColor(416)
    
    type2CorrTemplate.SetTitle("Correction Function Template")
    
    noise=0
    
    print "Find abort gap"
    gap=False
    idl=0
    num_cut=20
    for l in range(1,500):
        if allCorrLumiPerBX[LBKey].GetBinContent(l)==0 and allCorrLumiPerBX[LBKey].GetBinContent(l+1)==0 and allCorrLumiPerBX[LBKey].GetBinContent(l+2)==0:
            gap=True
        if gap and allCorrLumiPerBX[LBKey].GetBinContent(l)!=0 and idl<num_cut:
            noise+=allCorrLumiPerBX[LBKey].GetBinContent(l)
            idl+=1
    
    noise=noise/num_cut
         
    
    print "Apply and save type 1 corrections"
    if not args.noType1:
        for k in range(1,BXLength):
            bin_k = allCorrLumiPerBX[LBKey].GetBinContent(k)
            allCorrLumiPerBX[LBKey].SetBinContent(k+1, allCorrLumiPerBX[LBKey].GetBinContent(k+1)-bin_k*a1-bin_k*bin_k*a2)
            corrPerBX[LBKey].SetBinContent(k+1, corrPerBX[LBKey].GetBinContent(k+1)+bin_k*a1+bin_k*bin_k*a2)
    allLumiType1CorrPerBX[LBKey]=allCorrLumiPerBX[LBKey].Clone()
    allLumiType1CorrPerBX[LBKey].SetError(zeroes)
    
    for m in range(1,BXLength):
        allCorrLumiPerBX[LBKey].SetBinContent(m, allCorrLumiPerBX[LBKey].GetBinContent(m)-noise)
        noisePerBX[LBKey].SetBinContent(m, noise)
        corrPerBX[LBKey].SetBinContent(m, corrPerBX[LBKey].GetBinContent(m)+noise)
    
    
    print "Apply and save type 2 corrections"
    if not args.noType2:
        for i in range(1,BXLength):
            for j in range(i+1,BXLength):
                binsig_i=allCorrLumiPerBX[LBKey].GetBinContent(i)
                binfull_i=allLumiPerBX[LBKey].GetBinContent(i)
                if not args.useresponse:
                    allCorrLumiPerBX[LBKey].SetBinContent(j,allCorrLumiPerBX[LBKey].GetBinContent(j)-binsig_i*type2CorrTemplate.GetBinContent(j-i))
                    corrPerBX[LBKey].SetBinContent(j, corrPerBX[LBKey].GetBinContent(j)+binsig_i*type2CorrTemplate.GetBinContent(j-i))
                else:
                    allCorrLumiPerBX[LBKey].SetBinContent(j,allCorrLumiPerBX[LBKey].GetBinContent(j)-binfull_i*type2CorrTemplate.GetBinContent(j-i))
                    corrPerBX[LBKey].SetBinContent(j,corrPerBX[LBKey].GetBinContent(j)+binfull_i*type2CorrTemplate.GetBinContent(j-i))
    
    allLumiType1And2CorrPerBX[LBKey]=allCorrLumiPerBX[LBKey].Clone()
    allLumiType1And2CorrPerBX[LBKey].SetError(zeroes)
    
    print "Apply and save additional quadratic subtraction for trains",args.quadTrainCorr
    if args.quadTrainCorr != 0:
        #find train BXs
        trainBXs=[]
        trainBXs2=[]
        maxBX=0
        for ibx in range(1,BXLength):
            thisSBIL=allCorrLumiPerBX[LBKey].GetBinContent(ibx)
            if thisSBIL>maxBX:
                maxBX=thisSBIL
    
        #this ignores the leading bx-desired behavior
        print maxBX
        for ibx in range(2,BXLength):
            prevBXActive=(allCorrLumiPerBX[LBKey].GetBinContent(ibx-1)>maxBX*0.2)
            prevBXActive2=(allCorrLumiPerBX[LBKey].GetBinContent(ibx-1)>0.5)
            
            if prevBXActive:
                curBXActive=(allCorrLumiPerBX[LBKey].GetBinContent(ibx)>maxBX*0.2)
                if curBXActive:
                    trainBXs.append(ibx)
    
            if prevBXActive2:
                curBXActive2=(allCorrLumiPerBX[LBKey].GetBinContent(ibx)>0.5)
                if curBXActive2:
                    trainBXs2.append(ibx)

            print ibx,"prevlumi",allCorrLumiPerBX[LBKey].GetBinContent(ibx-1),prevBXActive,prevBXActive2,len(trainBXs),len(trainBXs2)
           
    
        print LBKey,"trainBXs",len(trainBXs)
        print LBKey,"trainBXs2",len(trainBXs2)
    
        for ibx in trainBXs:
            binsig_i=allCorrLumiPerBX[LBKey].GetBinContent(ibx)
            binfull_i=allLumiPerBX[LBKey].GetBinContent(ibx)
            allCorrLumiPerBX[LBKey].SetBinContent(ibx,binsig_i-args.quadTrainCorr*binsig_i*binsig_i)
            corrPerBX[LBKey].SetBinContent(ibx, corrPerBX[LBKey].GetBinContent(ibx)+args.quadTrainCorr*binsig_i*binsig_i)
        
    
    print "Finish up dividing plots"
    corrRatioPerBX[LBKey]=corrPerBX[LBKey].Clone()
    corrPerBX[LBKey].SetError(zeroes)
    corrRatioPerBX[LBKey].Divide(allLumiPerBX[LBKey])
    corrRatioPerBX[LBKey].SetError(zeroes)
    
    noiseToCorrRatio[LBKey]=noisePerBX[LBKey].Clone()
    noiseToCorrRatio[LBKey].Divide(corrPerBX[LBKey])
    noiseToCorrRatio[LBKey].SetError(zeroes)
    
    newfile.WriteTObject(allLumiPerBX[LBKey],  "Before_Corr_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(allLumiType1CorrPerBX[LBKey], "After_TypeI_Corr_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(allLumiType1And2CorrPerBX[LBKey], "After_TypeI_TypeII_Corr_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(allCorrLumiPerBX[LBKey], "After_Corr_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(noisePerBX[LBKey], "Noise_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(corrPerBX[LBKey], "Overall_Correction_"+Fill[LBKey]+"_"+LBKey)
    newfile.WriteTObject(corrRatioPerBX[LBKey], "Ratio_Correction_"+Fill[LBKey]+"_"+LBKey)
    #newfile.WriteTObject(ratio_gap, "Ratio_Nonlumi_"+LBKey)
    newfile.WriteTObject(noiseToCorrRatio[LBKey], "Ratio_Noise_"+Fill[LBKey]+"_"+LBKey)
