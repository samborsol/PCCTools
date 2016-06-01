import ROOT
import sys
import argparse

parser = argparse.ArgumentParser(description='Make standard plots from mini tree')
parser.add_argument('--minitree', type=str, default="", help="Mini tree file name")
parser.add_argument('--lsrange', default="0,400", help="Range of lumi sections to plot (default:  0,400)")
parser.add_argument('--batch', default=1, help="Run in batch mode (don't pop up canvases)")
args = parser.parse_args()

tfile=ROOT.TFile.Open(args.minitree)
ttree=tfile.Get("pccminitree")

if args.batch != 0:
    ROOT.gROOT.SetBatch(ROOT.kTRUE) 

lsRange=[]
for part in args.lsrange.split(","):
    lsRange.append(int(part))

nLS=lsRange[1]-lsRange[0]

nEntries=ttree.GetEntries()
can=ROOT.TCanvas("can","",800,600)

nWithOutNew=0
nLimit=100
BCIDs=[]
for iEnt in range(nEntries):
    ttree.GetEntry(iEnt)
    if ttree.BXid not in BCIDs:
        BCIDs.append(ttree.BXid)
        nWithOutNew=0
    else:
        nWithOutNew=nWithOutNew+1

    if nWithOutNew>nLimit:
        break

BCIDs.sort()

print BCIDs

LSRangeStr="LS>"+str(lsRange[0])+"&&LS<"+str(lsRange[1])
colors=[633,417,601,433,617]


eventRateHists={}
for BCID in BCIDs:
    eventRateHists[BCID]=ROOT.TH1F("rate"+str(BCID),";Lumi Section;Event Rate (Hz)",nLS,lsRange[0],lsRange[1])
    #eventRateHists[BCID]=ROOT.TH1F("rate"+str(BCID),"Rate of "+str(BCID)+";Lumi Section;Event Rate (Hz)",nLS,lsRange[0],lsRange[1])
eventRateHists["totalrate"]=ROOT.TH1F("totalrate","Total Rate;Lumi Section;Event Rate (Hz)",nLS,lsRange[0],lsRange[1])

iColor=0
for eventRateHistName in eventRateHists:
    eventRateHists[eventRateHistName].SetLineWidth(2)
    if eventRateHistName=="totalrate":
        ttree.Draw("LS>>totalrate","("+LSRangeStr+")/23.31","histgroff")
        eventRateHists[eventRateHistName].SetLineColor(1)
    else:
        ttree.Draw("LS>>rate"+str(eventRateHistName),"("+LSRangeStr+"&&BXid=="+str(eventRateHistName)+")/23.31","histgroff")
        eventRateHists[eventRateHistName].SetLineColor(colors[iColor%len(colors)])
        iColor=iColor+1


PCCRateHists={}
for BCID in BCIDs:
    PCCRateHists[BCID]=ROOT.TH1F("PCCrate"+str(BCID),";Lumi Section;PCC Rate (Clusters/Event)",nLS,lsRange[0],lsRange[1])
    #PCCRateHists[BCID]=ROOT.TH1F("PCCrate"+str(BCID),"Rate of "+str(BCID)+";Lumi Section;PCC Rate (Clusters/Event)",nLS,lsRange[0],lsRange[1])
PCCRateHists["PCCtotalrate"]=ROOT.TH1F("PCCtotalrate","Total Rate;Lumi Section;PCC Rate (Clusters/Event)",nLS,lsRange[0],lsRange[1])

iColor=0
for PCCRateHistName in PCCRateHists:
    PCCRateHists[PCCRateHistName].SetLineWidth(2)
    if PCCRateHistName=="PCCtotalrate":
        ttree.Draw("LS>>PCCtotalrate","("+LSRangeStr+")*nCluster","histgroff")
        PCCRateHists[PCCRateHistName].SetLineColor(1)
    else:
        ttree.Draw("LS>>PCCrate"+str(PCCRateHistName),"("+LSRangeStr+"&&BXid=="+str(PCCRateHistName)+")*nCluster","histgroff")
        PCCRateHists[PCCRateHistName].SetLineColor(colors[iColor%len(colors)])
        iColor=iColor+1
    PCCRateHists[PCCRateHistName].Divide(eventRateHists[eventRateHistName]*23.31)


VtxRateHists={}
for BCID in BCIDs:
    VtxRateHists[BCID]=ROOT.TH1F("Vtxrate"+str(BCID),";Lumi Section;Tight VTX Rate (Vertices/Event)",nLS,lsRange[0],lsRange[1])
    #VtxRateHists[BCID]=ROOT.TH1F("Vtxrate"+str(BCID),"Rate of "+str(BCID)+";Lumi Section;Tight VTX Rate (Vertices/Event)",nLS,lsRange[0],lsRange[1])
VtxRateHists["Vtxtotalrate"]=ROOT.TH1F("Vtxtotalrate","Total Rate;Lumi Section;Tight VTX Rate (Vertices/Event)",nLS,lsRange[0],lsRange[1])

iColor=0
for vtxRateHistName in VtxRateHists:
    VtxRateHists[vtxRateHistName].SetLineWidth(2)
    if vtxRateHistName=="Vtxtotalrate":
        ttree.Draw("LS>>Vtxtotalrate","("+LSRangeStr+")*nVtx","histgroff")
        VtxRateHists[vtxRateHistName].SetLineColor(1)
    else:
        ttree.Draw("LS>>Vtxrate"+str(vtxRateHistName),"("+LSRangeStr+"&&BXid=="+str(vtxRateHistName)+")*nVtx","histgroff")
        VtxRateHists[vtxRateHistName].SetLineColor(colors[iColor%len(colors)])
        iColor=iColor+1
    VtxRateHists[vtxRateHistName].Divide(eventRateHists[eventRateHistName]*23.31)




eventRateHists["totalrate"].Draw("hist")
can.Update()
can.SaveAs("totalEventRate_"+str(ttree.run)+".png")

first=True
leg=ROOT.TLegend(0.7,0.3,0.8,0.6)
for BCID in BCIDs:
    if first:
        eventRateHists[BCID].Draw("hist")
        first=False
    else:
        eventRateHists[BCID].Draw("histsame")
    leg.AddEntry(eventRateHists[BCID],str(BCID),"l")
        
leg.Draw("same")
can.Update()
can.SaveAs("eventRatePerBCID_"+str(ttree.run)+".png")



PCCRateHists["PCCtotalrate"].Draw("hist")
can.Update()
can.SaveAs("totalPCCRate_"+str(ttree.run)+".png")

first=True
leg=ROOT.TLegend(0.7,0.3,0.8,0.6)
for BCID in BCIDs:
    if first:
        PCCRateHists[BCID].Draw("hist")
        first=False
    else:
        PCCRateHists[BCID].Draw("histsame")
    leg.AddEntry(PCCRateHists[BCID],str(BCID),"l")
        
leg.Draw("same")
        
can.Update()
can.SaveAs("PCCRatePerBCID_"+str(ttree.run)+".png")



VtxRateHists["Vtxtotalrate"].Draw("hist")
can.Update()
can.SaveAs("totalVtxRate_"+str(ttree.run)+".png")

first=True
leg=ROOT.TLegend(0.7,0.3,0.8,0.6)
for BCID in BCIDs:
    if first:
        VtxRateHists[BCID].Draw("hist")
        first=False
    else:
        VtxRateHists[BCID].Draw("histsame")
    leg.AddEntry(VtxRateHists[BCID],str(BCID),"l")
        
leg.Draw("same")
        
can.Update()
can.SaveAs("vtxRatePerBCID_"+str(ttree.run)+".png")


