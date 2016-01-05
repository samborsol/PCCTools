import ROOT
import sys,os
import numpy
import array
import math
import argparse

parser = argparse.ArgumentParser(description='Process entries in event-based trees to produce pixel cluster counts')
parser.add_argument('--pccfile', type=str, default="", help='The pccfile to input (pixel clusters and vertices)')
parser.add_argument('--label', type=str, default="", help="Label for output file")
parser.add_argument('--mintime', type=float, default=0, help="Minimum time stamp")
parser.add_argument('--maxtime', type=float, default=math.pow(2,66), help="Maximum time stamp")
parser.add_argument('--vetoModules', type=str, default="vetoModules.txt", help="Text file containing list of pixel modules to veto (default: vetoModules.txt)")

args = parser.parse_args()


f_LHC = 11245.6
t_LS=math.pow(2,18)/f_LHC
xsec_mb=80000. #microbarn


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


weightThreshold=1e-5

def AverageWithWeight(list):
    sumValue=0
    sumWeight=0
    for value,weight in list:
        sumValue=sumValue+value
        sumWeight=sumWeight+weight

    if sumWeight>0:
        return float(sumValue)/sumWeight

def GetWeightedValues(list):
    count=0
    sumOfWeights=0
    sumOfWeights2=0
    weightedSum=0

    for value,weight in list:
        #print value,weight
        if weight<weightThreshold:
            continue
        count=count+1
        sumOfWeights=sumOfWeights+weight
        sumOfWeights2=sumOfWeights2+math.pow(weight,2)
        weightedSum=weightedSum+weight*value

    return count,sumOfWeights,sumOfWeights2,weightedSum


def GetMean(list):
    #print "list length",len(list)
    count,sumOfWeights,sumOfWeights2,weightedSum=GetWeightedValues(list)
    mean=GetMeanFromWeightedValues(sumOfWeights,weightedSum)
    return mean


def GetMeanFromWeightedValues(sumOfWeights,weightedSum):
    mean=0
    if sumOfWeights>0:
        mean=weightedSum/sumOfWeights
    return mean


def GetMeanAndMeanError(list):
    count,sumOfWeights,sumOfWeights2,weightedSum=GetWeightedValues(list)
    if sumOfWeights2==0:
        return -99,-99
    neff=math.pow(sumOfWeights,2)/sumOfWeights
    mean=GetMeanFromWeightedValues(sumOfWeights,weightedSum)

    #print neff,count,sumOfWeights
    
    weightedSumDiffFromAve2=0
    for value,weight in list:
        if weight<weightThreshold:
            continue
        weightedSumDiffFromAve2=weightedSumDiffFromAve2+weight*math.pow(value-mean,2) 

    stddev=0
    meanError=0
    if count>2:
        stddev=math.sqrt( weightedSumDiffFromAve2 / (sumOfWeights))
        meanError=stddev/math.sqrt(neff)

    #print "stddev",stddev

    return mean,meanError



#######################
#  Setup PCC Ntuples  #
#######################
if args.pccfile=="":
    print "pccfile is not given"
    sys.exit(1)

filename=args.pccfile

if filename.find("/store")==0: # file is in eos
    filename="root://eoscms//eos/cms"+filename

try:
    tfile=ROOT.TFile.Open(filename)
except:
    print filename,"failed to open properly"
    sys.exit(1)

tree=tfile.Get("lumi/tree")

tree.SetBranchStatus("*",0)
tree.SetBranchStatus("run",1)
tree.SetBranchStatus("LS",1)
tree.SetBranchStatus("event",1)
tree.SetBranchStatus("nPixelClusters",1)
tree.SetBranchStatus("layer*",1)
tree.SetBranchStatus("bunchCrossing",1)
tree.SetBranchStatus("timeStamp_begin",1)

#######################
# Make mod veto list  #
#######################
vetoModules=[]

if os.path.isfile(args.vetoModules):
    vetoFile=open(args.vetoModules)
    lines = vetoFile.readlines()
    for line in lines:
        for mod in line.split(","):
            try:
                vetoModules.append(int(mod))
            except:
                print "Error reading: ",mod,"in",line

else:
    print "Veto list does not exist... not vetoing anything."

print vetoModules


#######################
# Setup new mini-tree #
#######################
newfilename=filename.split("/")[-1].split(".")[0]+"_"+args.label+".root"

newfile=ROOT.TFile(newfilename,"recreate")
newtree=ROOT.TTree("pccminitree","pcc vdm scan data")

run             = array.array( 'l', [ 0 ] )
LS              = array.array( 'l', [ 0 ] )
event           = array.array( 'l', [ 0 ] )
timeStamp       = array.array( 'l', [ 0 ] )
BXid            = array.array( 'l', [ 0 ] )
nCluster        = array.array( 'd', [ 0 ] )
nClusterPerLayer= array.array( 'd', 5*[ 0 ] )


newtree.Branch("run",run,"run/I")
newtree.Branch("LS",LS,"LS/I")
newtree.Branch("event",event,"event/i")
newtree.Branch("timeStamp",timeStamp,"timeStamp/i")
newtree.Branch("BXid",BXid,"BXid/I")
newtree.Branch("nCluster",nCluster,"nCluster/D")
newtree.Branch("nClusterPerLayer",nClusterPerLayer,"nClusterPerLayer[5]/D")



#######################
#  Loop over events   #
#######################
nentries=tree.GetEntries()

print nentries
maxNBX=0
for iev in range(nentries):
    tree.GetEntry(iev)
    if iev%30000==0:
        print "iev,",iev
        print "(tree.run,tree.LS)",tree.LS
        print "len(tree.nPixelClusters)",len(tree.nPixelClusters)
        print "len(tree.layers)",len(tree.layers)
   
    if tree.timeStamp_begin<args.mintime or tree.timeStamp_begin>args.maxtime:
        continue

    pixelCount=[0]*6

    for item in tree.nPixelClusters:
        bxid=item[0][0]
        module=item[0][1]
        layer=tree.layers[module]
        clusters=item[1]

        if layer in vetoModules:
            continue

        if layer==6:
            layer=1

        pixelCount[layer]=pixelCount[layer]+clusters
        if layer!=1:
            pixelCount[0]=pixelCount[0]+clusters

    
    run[0]=tree.run
    LS[0]=tree.LS
    event[0]=tree.event
    timeStamp[0]=tree.timeStamp_begin
    BXid[0]=tree.bunchCrossing
    
    nCluster[0]=pixelCount[0]
    for layer in range(1,6):
        nClusterPerLayer[layer-1]=pixelCount[layer]

    newtree.Fill()


newfile.Write()
newfile.Close()

