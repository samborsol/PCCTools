import ROOT
import sys, os
import math

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def round_to_1(x):
    return round(x, -int(math.floor(math.log10(x))))

def round_to_reference(x, y):
    return round(x, -int(math.floor(math.log10(y))))


def SetNBX():
    lumiVars["HFLumi_perBX"]["nBX"]=tree.nBXHF
    lumiVars["BCMFLumi_perBX"]["nBX"]=tree.nBXBCMF
    lumiVars["PLTLumi_perBX"]["nBX"]=tree.nBXPLT
    lumiVars["PC_lumi_B3p8_perBX"]["nBX"]=tree.nBX
#    lumiVars["PC_lumi_layer2"]["nBX"]=tree.nBX


if len(sys.argv) <2:
    print "Please give the root as an argument"

fileName=sys.argv[1]
print fileName
tFile=ROOT.TFile.Open(fileName)
tree=tFile.Get("certtree")

# FIXME make dir if not there already
outDir="plots/"


lumiVars={}
lumiVars["HFLumi_perBX"]={}
lumiVars["BCMFLumi_perBX"]={}
lumiVars["PLTLumi_perBX"]={}
lumiVars["PC_lumi_B3p8_perBX"]={}
#lumiVars["PC_lumi_layer2"]={}

lumiVars["HFLumi_perBX"]["lumi"]=tree.HFLumi_perBX
lumiVars["BCMFLumi_perBX"]["lumi"]=tree.BCMFLumi_perBX
lumiVars["PLTLumi_perBX"]["lumi"]=tree.PLTLumi_perBX
lumiVars["PC_lumi_B3p8_perBX"]["lumi"]=tree.PC_lumi_B3p8_perBX
#lumiVars["PC_lumi_layer2"]["lumi"]=tree.nPCPerLayer[2]*tree.nActiveBX*2^18/(9.4e6*0.319)/23.31

lumiVars["HFLumi_perBX"]["nBX"]=tree.nBXHF
lumiVars["BCMFLumi_perBX"]["nBX"]=tree.nBXBCMF
lumiVars["PLTLumi_perBX"]["nBX"]=tree.nBXPLT
lumiVars["PC_lumi_B3p8_perBX"]["nBX"]=tree.nBX
#lumiVars["PC_lumi_layer2"]["nBX"]=tree.nBX


lumiVars["HFLumi_perBX"]["BX"]=tree.HFBXid
lumiVars["BCMFLumi_perBX"]["BX"]=tree.BCMFBXid
lumiVars["PLTLumi_perBX"]["BX"]=tree.PLTBXid
lumiVars["PC_lumi_B3p8_perBX"]["BX"]=tree.PCBXid
#lumiVars["PC_lumi_layer2"][""]=tree.PCBXid


lumiVars["HFLumi_perBX"]["activeBX"]={}
lumiVars["BCMFLumi_perBX"]["activeBX"]={}
lumiVars["PLTLumi_perBX"]["activeBX"]={}
lumiVars["PC_lumi_B3p8_perBX"]["activeBX"]={}
#lumiVars["PC_lumi_layer2"][""]=tree.



nEntries=tree.GetEntries()
# how many LSs to group together
nLS=200
minPCC=20
doFits=False
corrPCC=True

timeOrderedEntries=[]
runLSToEntry={}
maxLSInRun={}
#each entry is a LS
print "Looping for order,",nEntries
for iEnt in range(nEntries):
    tree.GetEntry(iEnt)
    SetNBX()

    if tree.run not in maxLSInRun.keys():
        maxLSInRun[tree.run]=0
    if tree.LS > maxLSInRun[tree.run]:
        maxLSInRun[tree.run]=tree.LS
    runLSToEntry[(tree.run,tree.LS)]=iEnt

runLSKeys=runLSToEntry.keys()
runLSKeys.sort()
for runLS in runLSKeys:
    timeOrderedEntries.append(runLSToEntry[runLS])



prevLSKey=[-99,-99]
print "Looping for active BXes,",nEntries


#HF=PC+1
#probably my fault in certtrees

LSperRun=0
LStoCheck=10
for iOrdered in timeOrderedEntries:
    tree.GetEntry(iOrdered)
    SetNBX()
    if tree.run!=prevLSKey[0]:
        #reset LS counter
        for lumiType in lumiVars:
            lumiVars[lumiType]["activeBX"][tree.run]=[]
        LSperRun=0

    if LSperRun>LStoCheck:
        continue
    #entries are now time ordered, but check
    if tree.run<prevLSKey[0]:
        print "Runs out of order"
        print prevLSKey,iEnt, tree.run, tree.LS
    elif tree.run==prevLSKey[0] and tree.LS<prevLSKey[1]:
        print "Same run, LSs out of order"
        print prevLSKey,iEnt, tree.run, tree.LS
    prevLSKey=[tree.run,tree.LS]

    #print prevLSKey,LSperRun 
    #print "loop HF for max"
    for lumiType in lumiVars:
        maxLumi=0
        for iBX in range(lumiVars[lumiType]["nBX"]):
            if lumiVars[lumiType]["lumi"][iBX]>maxLumi:
                maxLumi=lumiVars[lumiType]["lumi"][iBX]

        #print "maxLumi",maxLumi
        #print "loop for active"
        for iBX in range(lumiVars[lumiType]["nBX"]):
            if lumiVars[lumiType]["lumi"][iBX]> 0.2*maxLumi:
                if lumiVars[lumiType]["BX"][iBX] not in lumiVars[lumiType]["activeBX"][tree.run]:
                    lumiVars[lumiType]["activeBX"][tree.run].append(lumiVars[lumiType]["BX"][iBX])
    
    #for iBXPC in range(tree.nBX):
    #    if tree.PCBXid[iBXPC] not in activeBXFromPC[tree.run]:
    #        #print iBXPC,tree.PCBXid[iBXPC]
    #        activeBXFromPC[tree.run].append(tree.PCBXid[iBXPC])
    #
    #for iBXBCM1F in range(tree.nBXBCMF):
    #    if tree.BCMFBXid[iBXBCM1F] not in activeBXFromBCM[tree.run]:
    #        #print iBXPC,tree.PCBXid[iBXPC]
    #        activeBXFromBCM[tree.run].append(tree.BCMFBXid[iBXBCM1F])

    LSperRun=LSperRun+1


#for run in maxLSInRun:
#    for lumiType in lumiVars:
#        print lumiType,lumiVars[lumiType]["activeBX"][tree.run]



#for run in activeBXFromHF:
#    print "are active in HF and PC the same in",run
#    activeBXFromHF[run].sort()
#    activeBXFromPC[run].sort()
#    print activeBXFromHF[run]
#    print activeBXFromPC[run]
#    print "==?",activeBXFromHF[run]==activeBXFromPC[run]


# find solo bunches and trains
runsWith50ns=[254833]

for run in maxLSInRun:
    for lumiType in lumiVars:
        print lumiType,run,len(lumiVars[lumiType]["activeBX"][run])
        print lumiVars[lumiType]["activeBX"][run]


soloBunches={}
bunchTrains={}
for run in maxLSInRun:
    iBunch=0
    prevBunch=-99
    soloBunches[run]=[]
    bunchTrains[run]={}
    bxList=[]
    deltaBX=1
    if run in runsWith50ns:
        deltaBX=2
    for bx in lumiVars["HFLumi_perBX"]["activeBX"][run]:
        if prevBunch!=-99:
            if bx-prevBunch==deltaBX:
                bxList.append(prevBunch)
            else:
                if len(bxList)>1:
                    bunchTrains[run][iBunch]=bxList
                    iBunch=iBunch+1
                elif len(bxList)==0:
                    soloBunches[run].append(prevBunch)
                bxList=[]
        else:
            bxList=[]
                
        prevBunch=bx

        if bx == lumiVars["HFLumi_perBX"]["activeBX"][run][-1]:
            if len(bxList)>1:
                bunchTrains[run][iBunch]=bxList
                iBunch=iBunch+1
            elif len(bxList)==0:
                soloBunches[run].append(prevBunch)
            
print "n+1 bunch"
for run in maxLSInRun.keys():
    print run,
    for iTrain in bunchTrains[run]:
        print bunchTrains[run][iTrain][-1]+3,
    print

# instantiate plots
hists={}
hists["HFLumi_perBX"]={}
hists["BCMFLumi_perBX"]={}
hists["PLTLumi_perBX"]={}
hists["PC_lumi_B3p8_perBX"]={}

norms={}
norms["HFLumi_perBX"]={}
norms["BCMFLumi_perBX"]={}
norms["PLTLumi_perBX"]={}
norms["PC_lumi_B3p8_perBX"]={}


for run in maxLSInRun.keys():
    for histKey in hists:
        nBins=int(maxLSInRun[run])/int(nLS)+1
        #maxLSVal=float(nBins*nLS)
        hists[histKey][run]=ROOT.TH1F(histKey+str(run),histKey+" "+str(run),nBins,0.,maxLSInRun[run])#maxLSVal)
        hists[histKey][str(run)+"2d"]=ROOT.TH2F(histKey+str(run)+"2d",histKey+" "+str(run),nBins,0,maxLSInRun[run],3600,0,3600.)
        norms[histKey][run]=ROOT.TH1F(histKey+"norm"+str(run),histKey+" "+str(run),nBins,0.,maxLSInRun[run])
        norms[histKey][str(run)+"2d"]=ROOT.TH2F(histKey+"norm"+str(run)+"2dnorm",histKey+" "+str(run),nBins,0,maxLSInRun[run],3600,0,3600.)
        for iLS in range(1,nBins+1):
            for iTrain in bunchTrains[run]:
                nBunch=len(bunchTrains[run][iTrain])
                name=str(run)+"_train"
                if iTrain<10:
                    name=name+"00"
                elif iTrain<100:
                    name=name+"0"
                name=name+str(iTrain)+"_LSblock"
                if iLS<10:
                    name=name+"00"
                elif iLS<100:
                    name=name+"0"
                name=name+str(iLS)
                hists[histKey][name]=ROOT.TH1F(histKey+name,name,nBunch,0,nBunch)




print "Looping for filling plots,",nEntries
#tree.SetBranchStatus("HFLumi_perBX",1)
#tree.SetBranchStatus("BCMFLumi_perBX",1)
#tree.SetBranchStatus("PLTLumi_perBX",1)
#tree.SetBranchStatus("PC_lumi_B3p8_perBX",1)


# need to rebin the lumi data (done this way mainly for PClumi)
testLimit=-1
iCount=0
for iOrdered in timeOrderedEntries:
    if iCount>testLimit and testLimit>0:
        break
    if iCount%400==0:
        print "iCount",iCount
    iCount=iCount+1
    tree.GetEntry(iOrdered)
    SetNBX()
    for histType in hists:
        #print histType,lumiVars[histType]["nBX"]
        for ibx in range(lumiVars[histType]["nBX"]):
            #print lumiVars[histType]["BX"][ibx]
            if lumiVars[histType]["BX"][ibx] in lumiVars[histType]["activeBX"][tree.run]:
                #print "Filling",tree.LS,lumiVars[histType]["BX"][ibx],lumiVars[histType]["lumi"][ibx]
                # Need to shift HF and PLT back by 1
                #if tree.run<255000 and (histType.find("PC_lumi")!=-1 or histType.find("BCMFLumi")!=-1):
                #    hists[histType][str(tree.run)+"2d"].Fill(tree.LS,lumiVars[histType]["BX"][ibx],lumiVars[histType]["lumi"][ibx])
                #    norms[histType][str(tree.run)+"2d"].Fill(tree.LS,lumiVars[histType]["BX"][ibx],1.0)
                #else:
                
                # Two corrections for PCC
                # 1) 6-8 % correction to bx n if there is lumi in bx n-1
                # 2) longer range correction
                # total is about 12% after bunch train ends -- approximating 
                lumiVal=lumiVars[histType]["lumi"][ibx]
                if histType.find("PC")!=-1 and corrPCC:
                    if lumiVars[histType]["BX"][ibx]-1 in lumiVars[histType]["activeBX"][tree.run]:
                        prevLumiVal=lumiVars[histType]["lumi"][ibx-1]
                        #lumiVal=lumiVal/1.12
                        lumiVal=lumiVal-lumiVal*0.06-prevLumiVal*0.06
                        #lumiVal=lumiVal-lumiVal*0.04-prevLumiVal*0.08
                        #lumiVal=lumiVal-prevLumiVal*0.12
                    
                hists[histType][str(tree.run)+"2d"].Fill(tree.LS,lumiVars[histType]["BX"][ibx]-1,lumiVal)
                norms[histType][str(tree.run)+"2d"].Fill(tree.LS,lumiVars[histType]["BX"][ibx]-1,1.0)


can=ROOT.TCanvas("can","",700,700)
colors=[633,417,601,401,403,801]
styles=[24,25,26,27,28]


# renormalize data
for run in maxLSInRun.keys():
    for histType in hists:
        hists[histType][str(run)+"2d"].Divide(norms[histType][str(run)+"2d"])
        hists[histType][str(run)+"2d"].Draw("colz")
        can.Update()
        can.SaveAs(outDir+histType+str(run)+"2d.png")
        #can.SaveAs(outDir+histType+str(run)+"2d.C")

        norms[histType][str(run)+"2d"].Draw("colz")
        can.Update()
        can.SaveAs(outDir+histType+str(run)+"2dnorm.png")
        #can.SaveAs(outDir+histType+str(run)+"2dnorm.C")


## fill instantaneous rate plots
for run in maxLSInRun.keys():
    nBins=int(maxLSInRun[run])/int(nLS)+1
    for iLS in range(1,nBins+1):
        for iTrain in bunchTrains[run]:
            iPlot=0
            for histType in hists:
                name=str(run)+"_train"
                if iTrain<10:
                    name=name+"00"
                elif iTrain<100:
                    name=name+"0"
                name=name+str(iTrain)+"_LSblock"
                if iLS<10:
                    name=name+"00"
                elif iLS<100:
                    name=name+"0"
                name=name+str(iLS)
                nBunch=len(bunchTrains[run][iTrain])
                print name,run,iPlot
                iBX=1
                hists[histType][name].SetMarkerColor(colors[iPlot%len(colors)])
                hists[histType][name].SetMarkerStyle(styles[iPlot%len(styles)])
                for BX in bunchTrains[run][iTrain]: 
                    print "bin content at",iBX,hists[histType][str(run)+"2d"].GetBinContent(iLS,BX)
                    hists[histType][name].SetBinContent(iBX,hists[histType][str(run)+"2d"].GetBinContent(iLS,BX))
                    # FIXME need to update error calculation
                    #if histType.find("PC")!=-1 and norms[histType][str(run)+"2d"].GetBinContent(iLS,BX) > 0:
                    #    hists[histType][name].SetBinError(iBX,hists[histType][str(run)+"2d"].GetBinContent(iLS,BX)/math.sqrt(norms[histType][str(run)+"2d"].GetBinContent(iLS,BX)))
                    #else:
                    #    hists[histType][name].SetBinError(iBX,0)
                    iBX=iBX+1
                iPlot=iPlot+1

## plot SBIL 
for run in maxLSInRun.keys():
    nBins=int(maxLSInRun[run])/int(nLS)+1
    for iLS in range(1,nBins+1):
        for iTrain in bunchTrains[run]:
            iPlot=0
            leg=ROOT.TLegend(0.7,0.7,0.9,0.9)
            for histType in hists:
                name=str(run)+"_train"
                if iTrain<10:
                    name=name+"00"
                elif iTrain<100:
                    name=name+"0"
                name=name+str(iTrain)+"_LSblock"
                if iLS<10:
                    name=name+"00"
                elif iLS<100:
                    name=name+"0"
                name=name+str(iLS)
                nBunch=len(bunchTrains[run][iTrain])
                print name,run,iPlot
                if iPlot==0:
                    print "set max", hists[histType][name].GetMaximum(),hists["HFLumi_perBX"][name].GetMaximum()
                    hists[histType][name].SetMinimum(0.01)
                    hists[histType][name].SetMaximum(6)
                    hists[histType][name].SetTitle("Train "+str(iTrain)+" LS Block"+str(iLS)+";BX in Train;SBIL Hz/ub")
                    #hists[histType][name].SetMaximum(hists["HFLumi_perBX"][name].GetMaximum()*1.1)
                    hists[histType][name].Draw("p")
                else:
                    hists[histType][name].Draw("samep")
                leg.AddEntry(hists[histType][name],histType.split("_")[0],"p")
                iPlot=iPlot+1
            leg.Draw("same")
            can.Update()
            can.SaveAs(outDir+name+".png")
            #can.SaveAs(outDir+name+".C")



ratios={}
ratios["HFLumi_perBX"]={}
ratios["BCMFLumi_perBX"]={}
ratios["PLTLumi_perBX"]={}
ratios["PLTOverHF"]={}

ratioProfiles={}
ratioProfiles["HFLumi_perBX"]={}
ratioProfiles["BCMFLumi_perBX"]={}
ratioProfiles["PLTLumi_perBX"]={}
ratioProfiles["PLTOverHF"]={}

groups=["solo","first","train"]
legs={}
for run in maxLSInRun.keys():
    legs[run]={}
    nBins=int(maxLSInRun[run])/int(nLS)+1
    for histType in ratioProfiles:
        ratioProfiles[histType][run]={}
        for group in groups:
            ratioProfiles[histType][run][group]=ROOT.TProfile("profile"+group+str(run)+histType,group+str(run),60,0,3.5,0.95,1.10)

    for histType in ratios:
        ratios[histType][run]={}
        legs[run][histType]={}
        ratios[histType][run]["solo"]=ROOT.TGraph()
        ratios[histType][run]["solo"].SetTitle("Solo Bunches;"+histType+"/PCLumi;PLT Lumi (SBIL) [Hz/ub]")
        #legs[run][histType]["solo"]=ROOT.TLegend(0.7,0.7,0.9,0.9)
        legs[run][histType]["first"]=ROOT.TLegend(0.65,0.7,0.9,0.9)
        legs[run][histType]["train"]=ROOT.TLegend(0.65,0.7,0.9,0.9)
        #for iTrain in range(len(bunchTrains[run])):
        for iTrain in bunchTrains[run]:
            #ratios[histType][run][group]=ROOT.TH2F(histType+str(run)+group,histType+str(run)+group,100,0,6,100,0.2,2.0)
            ratios[histType][run]["first"+str(iTrain)]=ROOT.TGraph()
            ratios[histType][run]["first"+str(iTrain)].SetTitle("Leading Train Bunches;PLT Lumi (SBIL) [Hz/ub];"+histType+"/PCLumi")
            ratios[histType][run]["train"+str(iTrain)]=ROOT.TGraph()
            ratios[histType][run]["train"+str(iTrain)].SetTitle("Train Bunches;PLT Lumi (SBIL) [Hz/ub];"+histType+"/PCLumi")
            #ratios[histType][run]["train"+str(iTrain)]=ROOT.TGraph((len(bunchTrains[run][iTrain])-1)*nBins)
            legs[run][histType]["first"].AddEntry(ratios[histType][run]["first"+str(iTrain)],"Train "+str(iTrain),"p")
            legs[run][histType]["train"].AddEntry(ratios[histType][run]["train"+str(iTrain)],"Train "+str(iTrain)+" N_{bx}="+str(len(bunchTrains[run][iTrain])),"p")

print soloBunches
print bunchTrains


for run in maxLSInRun.keys():
    nBins=int(maxLSInRun[run])/int(nLS)+1
    for histType in ratios:
        iSolo=0
        print "solo",histType
        for soloBX in soloBunches[run]:
            for iLSBin in range(1,hists["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetNbinsX()+1):
                if histType=="PLTOverHF":
                    numlumi=hists["HFLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX) 
                    denomlumi=hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX) 
                elif norms["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX)>minPCC:
                    denomlumi=hists["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX)
                    numlumi=hists[histType][str(run)+"2d"].GetBinContent(iLSBin,soloBX)
                else:
                    denomlumi=0
                    numlumi=0
               
                ratio=0 
                if denomlumi>0:
                    ratio=numlumi/denomlumi
                    #ratioProfiles[histType][run]["solo"].Fill(denomlumi,ratio)
                    ratioProfiles[histType][run]["solo"].Fill(hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX),ratio)
                    ratios[histType][run]["solo"].SetPoint(iSolo,hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,soloBX),ratio)
                    iSolo=iSolo+1
                print iLSBin,soloBX,denomlumi,numlumi,ratio
       
        trainCounter=0
        for iTrain in bunchTrains[run]:
            print "train",iTrain,"size",len(bunchTrains[run][iTrain])

            iFirstBin=0
            iTrainBin=0
            iBX=0
            for BX in bunchTrains[run][iTrain]:
                for iLSBin in range(1,hists["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetNbinsX()+1):
                    print "iLSBin,",iLSBin,
                    if histType=="PLTOverHF":
                        numlumi=hists["HFLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX) 
                        denomlumi=hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX) 
                    elif norms["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX)>minPCC:
                        denomlumi=hists["PC_lumi_B3p8_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX)
                        numlumi=hists[histType][str(run)+"2d"].GetBinContent(iLSBin,BX)
                    else:
                        denomlumi=0
                        numlumi=0

                    if denomlumi>0:
                        ratio=numlumi/denomlumi
                        if iBX==0:
                            #print "first",trainCounter,iLSBin,BX,histType,numlumi,denomlumi,ratio
                            print "first",iFirstBin,BX,histType,numlumi,denomlumi,ratio
                            #ratios[histType][run]["first"+str(iTrain)].SetPoint(iFirstBin,denomlumi,ratio)
                            #ratioProfiles[histType][run]["first"].Fill(denomlumi,ratio)
                            ratios[histType][run]["first"+str(iTrain)].SetPoint(iFirstBin,hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX),ratio)
                            ratioProfiles[histType][run]["first"].Fill(hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX),ratio)
                            iFirstBin=iFirstBin+1
                        else:
                            trainBXBin=nBins*(iBX-1)+iLSBin
                            #print "train",trainBXBin,iBX-1,iLSBin,BX,histType,numlumi,denomlumi,ratio
                            print "train",trainCounter,iTrainBin,iLSBin,iBX,BX,histType,numlumi,denomlumi,ratio
                            #ratios[histType][run]["train"+str(iTrain)].SetPoint(trainBXBin,denomlumi,ratio)
                            #ratios[histType][run]["train"+str(iTrain)].SetPoint(iTrainBin,denomlumi,ratio)
                            #ratioProfiles[histType][run]["train"].Fill(denomlumi,ratio)
                            ratios[histType][run]["train"+str(iTrain)].SetPoint(iTrainBin,hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX),ratio)
                            ratioProfiles[histType][run]["train"].Fill(hists["PLTLumi_perBX"][str(run)+"2d"].GetBinContent(iLSBin,BX),ratio)
                            iTrainBin=iTrainBin+1
                iBX=iBX+1
            trainCounter=trainCounter+1

linearFitResults={}
fitFuncs={}
if doFits:
    for histType in ratioProfiles:
        linearFitResults[histType]={}
        fitFuncs[histType]={}
        for run in ratioProfiles[histType]:
            fitFuncs[histType][run]={}
            firstPro=True
            iGroup=0
            linearFitResults[histType][run]={}
            for group in groups:
                fitFuncs[histType][run][group]=ROOT.TF1("pol1"+group+str(run)+histType,"[0]+[1]*x")
                ratioProfiles[histType][run][group].Fit(fitFuncs[histType][run][group])
                try:
                    linearFitResults[histType][run][group]=[round_to_reference(fitFuncs[histType][run][group].GetParameter(0), fitFuncs[histType][run][group].GetParError(0)),round_to_reference(fitFuncs[histType][run][group].GetParameter(1), fitFuncs[histType][run][group].GetParError(1))]
                except:
                    print "failed to round",fitFuncs[histType][run][group].GetParameter(0), fitFuncs[histType][run][group].GetParError(0),fitFuncs[histType][run][group].GetParameter(1), fitFuncs[histType][run][group].GetParError(1)
                    linearFitResults[histType][run][group]=[-99,-99]


for histType in ratioProfiles:
    for run in ratioProfiles[histType]:
        iGroup=0
        leg=ROOT.TLegend(0.4,0.7,0.9,0.9)
        #can=ROOT.TCanvas("can","",700,700)
        for group in groups:
            ratioProfiles[histType][run][group].SetMarkerColor(colors[iGroup%len(colors)])
            ratioProfiles[histType][run][group].SetMarkerStyle(styles[iGroup%len(styles)])
            if doFits:
                fitFuncs[histType][run][group].SetLineColor(colors[iGroup%len(colors)])
            if iGroup==0:
                ratioProfiles[histType][run][group].SetTitle("Ratio Profile in "+str(run)+";PLT SBIL [Hz/ub];Ratio")
                ratioProfiles[histType][run][group].Draw()
                if histType.find("HFLumi")!=-1:
                    ratioProfiles[histType][run][group].SetMaximum(1.2)
                    ratioProfiles[histType][run][group].SetMinimum(0.95)
                else:
                    ratioProfiles[histType][run][group].SetMaximum(1.1)
                    ratioProfiles[histType][run][group].SetMinimum(0.95)
            else:
                ratioProfiles[histType][run][group].Draw("same")
            if doFits:
                fitFuncs[histType][run][group].Draw("same")
                leg.AddEntry(ratioProfiles[histType][run][group],group+"   "+str(linearFitResults[histType][run][group][1])+"*SBIL + "+str(linearFitResults[histType][run][group][0]),"p")
            else:
                leg.AddEntry(ratioProfiles[histType][run][group],group,"p")
            iGroup=iGroup+1
        leg.Draw("same")
        can.Update()
        can.SaveAs(outDir+"profiles_"+histType+"_"+str(run)+".png")
            

can=ROOT.TCanvas("can","",700,700)
multiGraphs={}

for histType in ratios:
    multiGraphs[histType]={}
    for run in maxLSInRun.keys():
        multiGraphs[histType][run]={}
        for group in groups: # different multigraphs for each
            multiGraphs[histType][run][group]=ROOT.TMultiGraph() 
            multiGraphs[histType][run][group].SetTitle(group+";PLT Lumi (SBIL) [Hz/ub];"+histType+"/PCLumi")
            histNames=ratios[histType][run].keys()
            histNames.sort()
            for histName in histNames: 
                if histName.find(group) != -1:
                    try:
                        iPlot=int(histName.split(group)[1])
                    except:
                        iPlot=1
                    
                    #print "filling",group,histName
                    ratios[histType][run][histName].SetMarkerColor(colors[iPlot%len(colors)])
                    ratios[histType][run][histName].SetMarkerStyle(styles[iPlot%len(styles)])
                    multiGraphs[histType][run][group].Add(ratios[histType][run][histName])
                
            multiGraphs[histType][run][group].Draw("AP")
            if group == "train" or group == "first":
                legs[run][histType][group].Draw("same")
                

            can.Update()
            can.SaveAs(outDir+histType+"OverPC_vsPC_"+group+"_"+str(run)+".png")
            #can.SaveAs(outDir+histType+"OverPC_vsPC_"+group+"_"+str(run)+".C")
