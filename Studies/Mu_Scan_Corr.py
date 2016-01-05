import sys, os
import ROOT
from ROOT import TFile, TCanvas
from ROOT import gStyle


# The Certification Tree file for BRIL Lumis
brilfilename=sys.argv[1]
# The Certification Tree file for PCC Lumis
pccfilename =sys.argv[2]
# The root file including the Correction functions
corrfilename=sys.argv[3]
# Choose the Correction Function by the run number
corr_run=sys.argv[4]

brilfile=ROOT.TFile(brilfilename)
briltree=brilfile.Get("certtree")

pccfile=ROOT.TFile(pccfilename)
pcctree=pccfile.Get("pccminitree")

corrfile=ROOT.TFile(corrfilename)
Beforehist=corrfile.Get("Before_Corr_"+corr_run)
Afterhist=corrfile.Get("After_Corr_"+corr_run)
#corrhist=corrfile.Get("Ratio_Correction_"+corr_run)

outfile=ROOT.TFile("test_Linearity_corrected"+corr_run+".root", "recreate")

c=TCanvas("c", "c", 800, 800)
c.cd()

PCCHF=ROOT.TH2F("PCCHF", "PCCHF",2500,0, 2500, 2500, 0, 2500)
PCCBCMF=ROOT.TH2F("PCCBCMF", "PCCBCMF", 2500, 0, 2500, 2500, 0, 2500)
PCCPLT=ROOT.TH2F("PCCPLT", "PCCPLT", 2500, 0, 2500, 2500, 0, 2500)

briltree.SetBranchStatus("*",0)
briltree.SetBranchStatus("run",1)
briltree.SetBranchStatus("LS", 1)
briltree.SetBranchStatus("HFLumi", 1)
briltree.SetBranchStatus("BCMFLumi", 1)
briltree.SetBranchStatus("PLTLumi", 1)

pcctree.SetBranchStatus("*",0)
pcctree.SetBranchStatus("run", 1)
pcctree.SetBranchStatus("LS", 1)
pcctree.SetBranchStatus("step", 1)
pcctree.SetBranchStatus("nCluster", 1)
pcctree.SetBranchStatus("nClusterPerLayer", 1)
pcctree.SetBranchStatus("BXid", 1)

LSlist = [106, 109, 112, 114, 115, 117, 118, 120, 121, 123, 124, 126, 129, 132, 134, 135, 137, 138, 140, 141, 143, 146]

LSdict = { 106:3, 109:4, 112:5, 114:6, 115:6, 117:7, 118:7, 120:8, 121:8, 123:9, 124:9, 126:10, 129:11, 132:12, 134:13, 135:13, 137:14, 138:14, 140:15, 141:15, 143:16, 146:17}

HFstepdict ={3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[]}

BCMFstepdict={3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:  [], 16:[], 17:[]}

PLTstepdict={3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:  [], 16:[], 17:[]}

PCCstepdict={3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0], 7:[0,0], 8:[0,0], 9:[0,0], 10:[0,0], 11:[0,0], 12:[0,0], 13:[0,0], 14:[0,0], 15:  [0,0], 16:[0,0], 17:[0,0]}


HFLumidict={3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0}
BCMFLumidict={3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0}
PLTLumidict={3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0}
PCCLumidict={3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0}

b_nentries=briltree.GetEntries()
pcc_nentries=pcctree.GetEntries()

for i_bev in range(b_nentries):
    briltree.GetEntry(i_bev)
    if briltree.run==257734 and briltree.LS in LSlist:
        #print i_bev, briltree.run, briltree.LS, briltree.HFLumi, LSdict[briltree.LS]
        HFstepdict[LSdict[briltree.LS]].append(briltree.HFLumi)
        BCMFstepdict[LSdict[briltree.LS]].append(briltree.BCMFLumi)
        PLTstepdict[LSdict[briltree.LS]].append(briltree.PLTLumi)


for j in HFstepdict.keys():
    if len(HFstepdict[j])==1:
        HFLumidict[j]=HFstepdict[j][0]
        BCMFLumidict[j]=BCMFstepdict[j][0]
        PLTLumidict[j]=PLTstepdict[j][0]

    else:
        HFLumidict[j]=(HFstepdict[j][0]+HFstepdict[j][1])/2
        BCMFLumidict[j]=(BCMFstepdict[j][0]+BCMFstepdict[j][1])/2
        PLTLumidict[j]=(PLTstepdict[j][0]+PLTstepdict[j][1])/2

for i_pev in range(pcc_nentries):
    if i_pev%10000==0:
        print i_pev
    pcctree.GetEntry(i_pev)
    #if i_pev%10000==0:
    #    print "BXid,", pcctree.BXid
    #    print "correction, ", corrhist.GetBinContent(pcctree.BXid+1)
    if pcctree.run==257734 and PCCstepdict.has_key(pcctree.step):

        PCCstepdict[pcctree.step][0]+=pcctree.nCluster*Afterhist.GetBinContent(pcctree.BXid+1)/Beforehist.GetBinContent(pcctree.BXid+1)#(1-corrhist.GetBinContent(pcctree.BXid+1))
        PCCstepdict[pcctree.step][1]+=1

for k in PCCstepdict.keys():
    PCCLumidict[k]=PCCstepdict[k][0]/PCCstepdict[k][1]
print PCCLumidict

print HFLumidict
print BCMFLumidict
print PLTLumidict

for l in PCCLumidict.keys():
    PCCHF.Fill(PCCLumidict[l], HFLumidict[l], 1)
    PCCBCMF.Fill(PCCLumidict[l], BCMFLumidict[l], 1)
    PCCPLT.Fill(PCCLumidict[l], PLTLumidict[l], 1)
PCCHF.GetXaxis().SetTitle("PCC Lumi")
PCCHF.GetYaxis().SetTitle("HF Lumi")

PCCBCMF.GetXaxis().SetTitle("PCC Lumi")
PCCBCMF.GetYaxis().SetTitle("BCMF Lumi")

PCCPLT.GetXaxis().SetTitle("PCC Lumi")
PCCPLT.GetYaxis().SetTitle("PLT Lumi")

PCCHF.SetMarkerStyle(22)
PCCBCMF.SetMarkerStyle(26)
PCCPLT.SetMarkerStyle(21)

PCCHF.SetMarkerColor(2)
PCCBCMF.SetMarkerColor(4)
PCCPLT.SetMarkerColor(3)

PCCHF.Draw()
PCCBCMF.Draw("SAME")
PCCPLT.Draw("SAME")

c.SaveAs("test.png")

outfile.WriteTObject(PCCHF, "PCCHF")
outfile.WriteTObject(PCCBCMF,"PCCBCMF")
outfile.WriteTObject(PCCPLT, "PCCPLT")
outfile.Close()
#print BCMFstepdict
#print PLTstepdict
