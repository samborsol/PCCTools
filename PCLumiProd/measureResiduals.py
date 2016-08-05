import ROOT
import sys
import os
import argparse
import json
from ROOT import kBlue,TF1
ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser=argparse.ArgumentParser()
#parser.add_argument("-h",  "--help", help="Print these messages.")
parser.add_argument("-d",  "--dir",  default="",  help="Directory where derived corrections with type 2 only are located.")
parser.add_argument("-f",  "--file", default="",  help="File of derived corrections is located.")
parser.add_argument("-l",  "--label",default="",  help="Append the names of output files with this label.")
parser.add_argument("-j",  "--json", default="",  help="Certification JSON file for selecting runs.")
args=parser.parse_args()

runSelection={}
if args.json !="":
    certfile=open(args.json)
    runSelection=json.load(certfile)
    certfile.close()

filenames=[]
if args.dir!="":
    shortfilenames=os.listdir(args.dir)

    for shortfilename in shortfilenames:
        if shortfilename.find("Overall_")!=-1:
            filenames.append(args.dir+"/"+shortfilename)
if args.file!="":
    filenames.append(args.file)

#Fill   Bfield    Runs 
fillInfo={}

fillInfo["4647"]=["3.798513298",[262325,262326,262327,262328]]
fillInfo["4643"]=["3.798513298",[262270,262271,262272,262273,262274,262275,262277]]
fillInfo["4640"]=["3.798513298",[262248,262249,262250,262252,262253,262254]]
fillInfo["4639"]=["3.798513298",[262235]]
fillInfo["4638"]=["3.798513298",[262204,262205]]
fillInfo["4634"]=["3.798513298",[262081,262114,262121,262137,262147,262156,262157,262163,262164,262165,262167,262168,262169,262170,262171,262172,262173,262174]]
fillInfo["4569"]=["3.798970769",[260627]]
fillInfo["4565"]=["3.798970769",[260593]]
fillInfo["4562"]=["3.798970769",[260575,260576,260577]]
fillInfo["4560"]=["1.544083541",[260488,260489,260490,260491,260492,260493,260496,260497,260498,260499,260510,260527,260528,260532,260533,260534,260536,260538,260540,260541]]
fillInfo["4557"]=["3.719991773",[260424,260425,260426,260427,260431,260433,260439]]
fillInfo["4555"]=["3.80020411",[260373]]
fillInfo["4545"]=["0.019018997",[260230,260232,260233,260234,260235]]
fillInfo["4540"]=["0.019018997",[260099,260100,260101,260102,260104,260105,260107,260108,260114,260119,260132,260135,260136]]
fillInfo["4538"]=["0.019018997",[260034,260035,260036,260037,260038,260039,260041,260043,260061,260062,260066]]
fillInfo["4536"]=["0.019018997",[259968,259971,259972,259973]]
fillInfo["4532"]=["3.800569273",[259884,259890,259891]]
fillInfo["4530"]=["3.800569273",[259861,259862]]
fillInfo["4528"]=["3.800569273",[259809,259810,259811,259812,259813,259817,259818,259820,259821,259822]]
fillInfo["4525"]=["3.800569273",[259721]]
fillInfo["4522"]=["3.800569273",[259681,259682,259683,259685,259686]]
fillInfo["4519"]=["3.800569273",[259636,259637]]
fillInfo["4518"]=["3.800569273",[259626]]
fillInfo["4513"]=["3.800569273",[259464]]
fillInfo["4511"]=["3.800569273",[259429,259431]]
fillInfo["4510"]=["3.800569273",[259399]]
fillInfo["4509"]=["3.800569273",[259384,259385,259388]]
fillInfo["4505"]=["3.800569273",[259351,259352,259353]]
fillInfo["4499"]=["3.800569273",[259236,259237]]
fillInfo["4496"]=["3.800569273",[259199,259200,259201,259202,259204,259205,259207,259208]]
fillInfo["4495"]=["3.800569273",[259152,259157,259158,259159,259161,259162,259163,259164,259167]]
fillInfo["4485"]=["3.800569273",[258741,258742,258745,258749,258750]]
fillInfo["4479"]=["3.800569273",[258702,258703,258705,258706,258712,258713,258714]]
fillInfo["4477"]=["3.800569273",[258694]]
fillInfo["4476"]=["3.800569273",[258655,258656]]
fillInfo["4467"]=["3.800569273",[258425,258426,258427,258428,258432,258434,258440,258442,258443,258444,258445,258446,258448]]
fillInfo["4466"]=["3.800569273",[258403]]
fillInfo["4464"]=["3.799768191",[258335]]
fillInfo["4463"]=["3.799768191",[258312,258313,258319,258320]]
fillInfo["4462"]=["3.799768191",[258287]]
fillInfo["4455"]=["3.799768191",[258211,258213,258214,258215]]
fillInfo["4452"]=["3.799768191",[258174,258175,258177]]
fillInfo["4449"]=["3.799768191",[258157,258158,258159]]
fillInfo["4448"]=["3.799768191",[258129,258136]]
fillInfo["4444"]=["3.799768191",[257968,257969]]
fillInfo["4440"]=["3.799768191",[257804,257805,257816,257818,257819,257821,257822,257823,257824,257825]]
fillInfo["4437"]=["3.799768191",[257750,257751]]
fillInfo["4435"]=["3.799768191",[257721,257722,257723,257725,257732,257733,257734,257735]]
fillInfo["4434"]=["3.799768191",[257682]]
fillInfo["4432"]=["3.799768191",[257645]]
fillInfo["4428"]=["3.799768191",[257613,257614]]
fillInfo["4426"]=["3.799768191",[257599]]
fillInfo["4423"]=["3.799768191",[257531]]
fillInfo["4420"]=["3.799768191",[257487,257490]]
fillInfo["4418"]=["3.799768191",[257461]]
fillInfo["4410"]=["3.799768191",[257394,257395,257396,257397,257398,257399,257400]]
fillInfo["4402"]=["1.68653331",[257027,257032,257035,257038,257042,257044,257055,257058,257059]]
fillInfo["4398"]=["3.799673444",[256936,256941]]
fillInfo["4397"]=["3.799673444",[256926]]
fillInfo["4393"]=["3.799673444",[256866,256867,256868,256869]]
fillInfo["4391"]=["3.799673444",[256842,256843]]
fillInfo["4386"]=["3.799673444",[256801]]
fillInfo["4384"]=["3.799673444",[256728,256729,256730,256733,256734]]
fillInfo["4381"]=["3.799673444",[256673,256674,256675,256676,256677]]
fillInfo["4376"]=["3.799673444",[256630]]
fillInfo["4364"]=["0.018967839",[256464]]
fillInfo["4363"]=["0.018967839",[256443,256444,256445,256446,256447,256448]]
fillInfo["4360"]=["0.018967839",[256423,256424]]
fillInfo["4356"]=["0.018967839",[256405,256406]]
fillInfo["4349"]=["0.018967839",[256347,256348,256349,256350,256353,256355]]
fillInfo["4342"]=["0.018967839",[256245]]
fillInfo["4341"]=["0.018967839",[256234,256235,256236,256237]]
fillInfo["4337"]=["0.018967839",[256214,256215,256216,256217]]
fillInfo["4332"]=["0.018967839",[256167,256168,256169,256171]]
fillInfo["4323"]=["0.018967839",[256001,256002,256003,256004]]
fillInfo["4322"]=["0.018967839",[255981,255982,255983,255984,255985,255986,255987,255988,255989,255990,255993]]
fillInfo["4269"]=["3.799233459",[255019,255029,255030,255031]]
fillInfo["4268"]=["3.799233459",[255003]]
fillInfo["4266"]=["3.799233459",[254980,254982,254983,254984,254985,254986,254987,254989,254991,254992,254993]]
fillInfo["4257"]=["3.799233459",[254914]]
fillInfo["4256"]=["3.799233459",[254905,254906,254907]]
fillInfo["4254"]=["3.799233459",[254879]]
fillInfo["4249"]=["3.799233459",[254852]]
fillInfo["4246"]=["3.799233459",[254833]]
fillInfo["4243"]=["3.799233459",[254790]]
fillInfo["4231"]=["0.019004049",[254608]]
fillInfo["4225"]=["0.019004049",[254532]]
fillInfo["4224"]=["0.019004049",[254512]]
fillInfo["4220"]=["0.019004049",[254437,254450,254451,254453,254454,254455,254456,254457,254458,254459]]
fillInfo["4219"]=["0.019004049",[254416]]
fillInfo["4214"]=["0.019004049",[254380]]
fillInfo["4212"]=["0.019004049",[254362,254364,254366,254367,254368]]
fillInfo["4211"]=["0.019004049",[254349]]
fillInfo["4210"]=["0.019004049",[254340,254341,254342]]
fillInfo["4208"]=["0.019004049",[254332]]
fillInfo["4207"]=["0.019004049",[254306,254307,254308,254309,254310,254313,254314,254315,254316,254317,254318,254319]]
fillInfo["4205"]=["1.151918971",[254280,254282,254283,254284,254285,254289,254290,254292,254293,254294]]
fillInfo["4201"]=["3.800328948",[254227,254229,254230,254231,254232]]
fillInfo["4020"]=["0.018957838",[252126]]
fillInfo["4019"]=["0.018957838",[252116]]
fillInfo["4008"]=["3.799702722",[251883]]
fillInfo["4006"]=["3.799702722",[251864]]
fillInfo["4001"]=["3.799702722",[251781]]
fillInfo["3996"]=["3.799702722",[251717,251718,251721]]
fillInfo["3992"]=["3.799702722",[251636,251638,251640,251642,251643]]
fillInfo["3988"]=["3.799702722",[251559,251560,251561,251562]]
fillInfo["3986"]=["3.799702722",[251548]]
fillInfo["3983"]=["3.799702722",[251521,251522,251523]]
fillInfo["3981"]=["2.849426279",[251491,251493,251496,251497,251498,251499,251500]]
fillInfo["3976"]=["3.799731187",[251244,251249,251250,251251,251252]]
fillInfo["3974"]=["3.799731187",[251131,251134,251142,251143,251147,251149,251150,251153,251155,251156,251160,251161,251162,251163,251164,251167,251168,251170]]
fillInfo["3971"]=["3.799731187",[251022,251023,251024,251025,251026,251027,251028]]
fillInfo["3965"]=["0.018936371",[250930,250931,250932]]
fillInfo["3962"]=["0.036359372",[250885,250886,250889,250890,250891,250892,250893,250895,250896,250897,250898,250899,250901,250902]]
fillInfo["3960"]=["0.018828806",[250862,250863,250864,250865,250866,250867,250868,250869,250871]]
fillInfo["3858"]=["0.018828806",[248025,248026,248027,248028,248029,248030,248031,248032,248033,248035,248036,248037,248038]]
fillInfo["3857"]=["0.018828806",[247981,247982,247983,247987,247989,247990,247991,247992,247994,247996,247998,248000,248002,248003,248004,248005,248006,248007,248009]]
fillInfo["3855"]=["0.018828806",[247910,247911,247912,247913,247914,247915,247917,247919,247920,247921,247923,247924,247926,247927,247928,247931,247933,247934]]
fillInfo["3851"]=["0.018828806",[247702,247703,247704,247705,247707,247708,247710,247711,247716,247718,247719,247720]]
fillInfo["3850"]=["0.018828806",[247685]]
fillInfo["3848"]=["0.018828806",[247642,247644,247646,247647,247648]]
fillInfo["3847"]=["0.018828806",[247623]]
fillInfo["3846"]=["0.018828806",[247607,247609,247610,247611,247612]]
fillInfo["3835"]=["0.018828806",[247377,247379,247380,247381,247382,247383,247384,247385,247386,247387,247388,247389,247394,247395,247397,247398]]
fillInfo["3833"]=["0.018828806",[247302,247303,247305,247306,247307,247309,247310,247313,247317,247318,247319,247320,247323,247324,247326,247328,247333,247334,247335,247336]]
fillInfo["3829"]=["0.018828806",[247231,247232,247233,247234,247235,247236,247237,247238,247240,247241,247243,247244,247245,247246,247247,247248,247250,247251,247252,247253,247255,247256,247259,247261,247262,247263,247265,247266,247267]]
fillInfo["3824"]=["0.018828806",[247068,247069,247070,247073,247076,247077,247078,247079,247081]]
fillInfo["3820"]=["0.018842477",[246951,246953,246954,246956,246957,246958,246959,246960,246961,246962,246963]]
fillInfo["3819"]=["0.0188423",[246908,246912,246913,246914,246919,246920,246923,246926,246930,246933,246934,246936]]

def GetGaussianMeanError(hist):
    fun1 = TF1("fun1", "gaus", -0.03, 0.1)
    hist.Fit(fun1, "R")
    MeanError=[fun1.GetParameter(1), fun1.GetParameter(2)]
    return MeanError

def findRunInFill(run):
    for fill in fillInfo:
        if int(run) in fillInfo[fill][1]:
            return fill


if args.json !="":
    fillSelection=[]
    for run in runSelection:
        thisFill=findRunInFill(run)
        if thisFill not in fillSelection:
            fillSelection.append(thisFill)
    fillSelection.sort()




hists={}
can=ROOT.TCanvas("can","",1000,700)
if args.label!="":
    outRootFileName="systematicHistograms_"+args.dir+"_"+args.label+".root"
    outCVSFileName="summary_"+args.dir+"_"+args.label+".csv"
else:
    outRootFileName="systematicHistograms_"+args.dir+".root"
    outCVSFileName="summary_"+args.dir+".csv"
    
oFile=ROOT.TFile(outRootFileName,"RECREATE")
csvSummary=open(outCVSFileName,"w+")
type1ValueError={}
type1ValueErrorClean={}

type2ValueError={}
type2ValueErrorClean={}

filenames.sort()

nCount=0
nClean=0
for filename in filenames:
    try:
        tfile=ROOT.TFile.Open(filename)
        f1keys=tfile.GetListOfKeys()
    except:
        continue
    
    fHistNames=[]
    
    for f1key in f1keys:
        if f1key.GetName().find("After_Corr_")!=-1:
            fHistNames.append(f1key.GetName())
    
    for fHistName in fHistNames:
        tfile.cd() 
        #print fHistName
        #thisRun=fHistName.split("_")[2]
        #thisFill=findRunInFill(thisRun)
        thisFill=fHistName.split("_")[2]
        
        #if args.json!="":

        #if thisFill not in fillSelection:
        #if thisFill!="4947":
        #    continue


        hists[fHistName]=tfile.Get(fHistName)
        oFile.cd() 
        if hists[fHistName].Integral() < 0.0005*3600:
            print "Histogram contains only data from noise... skipping"
            continue

        hists[fHistName+"TrailingRatios"]=ROOT.TH1F(fHistName+"TrailingRatios",";Type 1 Fraction from after BX train;"+fHistName,200,-0.03,0.15)
        hists[fHistName+"Type2Residuels"]=ROOT.TH1F(fHistName+"Type2Residuels",";Type 2 residual (Hz/ub);"+fHistName,200,-0.02,0.15)
        
        lastBX=-1

        nActiveBX=0
        for ibx in range(2,hists[fHistName].GetNbinsX()-2):
            lumiM1=hists[fHistName].GetBinContent(ibx-1)
            lumi=hists[fHistName].GetBinContent(ibx)
            lumiP1=hists[fHistName].GetBinContent(ibx+1)
            lumiP2=hists[fHistName].GetBinContent(ibx+2)
            # Is bunch active?
            # Needs to be more than noise and less than lumi
            threshold=0.5
            if lumi>threshold: 
                nActiveBX=nActiveBX+1
                # is leading?
                #if lumiM1<threshold:
                # is last active bx?
                #if lumiP1<threshold:# and lumiP2<threshold: next is non-active
                if lumiP1<threshold and lumiP2<threshold: # end of train
                    lastBX=ibx
                    hists[fHistName+"TrailingRatios"].Fill(lumiP1/lumi)
                    print ibx,lumiP1,lumi,lumiP1/lumi
            
            # how is type 2 doing?
            # from 2 bx beyond a train to 30 or next active BX
            if lastBX>0 and ibx-lastBX>1 and ibx-lastBX<30:
                hists[fHistName+"Type2Residuels"].Fill(lumi)

        if nActiveBX==0:
            print "No active BXs in",fHistName
            continue
    
        can.cd()
        hists[fHistName+"TrailingRatios"].Draw()
        #hists[fHistName+"TrailingRatios"].Write()
        can.Update()
        #print "means",hists[fHistName+"TrailingRatios"].GetMean()
        #print "stdev",hists[fHistName+"TrailingRatios"].GetRMS()
        
    
        hists[fHistName+"Type2Residuels"].Draw()
        #hists[fHistName+"Type2Residuels"].Write()
        can.Update()
        #print "Type2 residuels",hists[fHistName+"Type2Residuels"].GetMean()
        #print "Type2 resid RMS",hists[fHistName+"Type2Residuels"].GetRMS()
   
        #print GetGaussianMeanError(hists[fHistName+"TrailingRatios"])
        type1MeanError = GetGaussianMeanError(hists[fHistName+"TrailingRatios"])
        csvSummary.write(fHistName+","+str(type1MeanError[0])+","+str(type1MeanError[1])+","+str(hists[fHistName+"Type2Residuels"].GetMean())+","+str(hists[fHistName+"Type2Residuels"].GetRMS())+"\n")
       
        if not type1ValueError.has_key(thisFill):
            type1ValueError[thisFill]={}
            type1ValueErrorClean[thisFill]={}
                
        if not type2ValueError.has_key(thisFill):
            type2ValueError[thisFill]={}
            type2ValueErrorClean[thisFill]={}
        nCount=nCount+1
        type1ValueError[thisFill][fHistName]=type1MeanError#[hists[fHistName+"TrailingRatios"].GetMean(),hists[fHistName+"TrailingRatios"].GetMeanError()]
        type2ValueError[thisFill][fHistName]=[hists[fHistName+"Type2Residuels"].GetMean(),hists[fHistName+"Type2Residuels"].GetMeanError()]

        if hists[fHistName+"TrailingRatios"].GetMeanError() <0.005 and hists[fHistName+"Type2Residuels"].GetMeanError()<0.00050 and hists[fHistName+"Type2Residuels"].GetMeanError()!=0:
            if hists[fHistName+"TrailingRatios"].GetMean()<-0.04:
                print fHistName+"TrailingRatios is",hists[fHistName+"TrailingRatios"].GetMean(),"looks dubious... skipping... need better criteria for skipping"
                continue
            type2ValueErrorClean[thisFill][fHistName]=[hists[fHistName+"Type2Residuels"].GetMean(),hists[fHistName+"Type2Residuels"].GetMeanError()]
            type1ValueErrorClean[thisFill][fHistName]=type1MeanError#[hists[fHistName+"TrailingRatios"].GetMean(),hists[fHistName+"TrailingRatios"].GetMeanError()]
            nClean=nClean+1
        #if hists[fHistName+"Type2Residuels"].GetMeanError() <0.005 :
        #hists[fHistName+"TrailingRatios"].Write()
        #hists[fHistName+"Type2Residuels"].Write()


csvSummary.write("\n\n")

oFile.cd() 
type1OverTime={}
type1OverTimeClean={}
fills=type1ValueError.keys()
type2OverTime={}
type2OverTimeClean={}
fills=type2ValueError.keys()
fills.sort()
labels1=";Blocks of 50 LSs;Type 1 Fraction"
labels2=";Blocks of 50 LSs;Type 2 SBIL"
type1OverTime["all"]=ROOT.TH1F("type1OverTimeAll",labels1,nCount,0,nCount)
type1OverTimeClean["all"]=ROOT.TH1F("type1OverTimeCleanAll",labels1,nClean,0,nClean)
type2OverTime["all"]=ROOT.TH1F("type2OverTimeAll",labels2,nCount,0,nCount)
type2OverTimeClean["all"]=ROOT.TH1F("type2OverTimeCleanAll",labels2,nClean,0,nClean)

tgraph1=ROOT.TGraphErrors()
tgraph2=ROOT.TGraphErrors()
tgraph1.SetTitle(";Fill;Type 1 residual (Fraction)")
tgraph2.SetTitle(";Fill;Type 2 residual (SBIL,Hz/#mub)")
tgraph1.SetName("type1FracPerFill")
tgraph2.SetName("type2SBILPerFill")

iFill=0

iCountAll=1
iCleanAll=1
for fill in fills:
    type1OverTime[fill]=ROOT.TH1F("type1OverTime"+str(fill),labels1,len(type1ValueError[fill]),0,len(type1ValueError[fill]))
    type2OverTime[fill]=ROOT.TH1F("type2OverTime"+str(fill),labels2,len(type2ValueError[fill]),0,len(type2ValueError[fill]))
    LSBlockNames=type1ValueError[fill].keys()
    LSBlockNames.sort()
    iCount=1
    for LSBlock in LSBlockNames:
        type1OverTime[fill].SetBinContent(iCount,type1ValueError[fill][LSBlock][0])
        type1OverTime[fill].SetBinError(iCount,type1ValueError[fill][LSBlock][1])
        type2OverTime[fill].SetBinContent(iCount,type2ValueError[fill][LSBlock][0])
        type2OverTime[fill].SetBinError(iCount,type2ValueError[fill][LSBlock][1])
        iCount=iCount+1
    
        type1OverTime["all"].SetBinContent(iCountAll,type1ValueError[fill][LSBlock][0])
        type1OverTime["all"].SetBinError(iCountAll,type1ValueError[fill][LSBlock][1])
        type2OverTime["all"].SetBinContent(iCountAll,type2ValueError[fill][LSBlock][0])
        type2OverTime["all"].SetBinError(iCountAll,type2ValueError[fill][LSBlock][1])
        iCountAll=iCountAll+1
    
    type1OverTimeClean[fill]=ROOT.TH1F("type1OverTimeClean"+str(fill),labels1,len(type1ValueErrorClean[fill]),0,len(type1ValueErrorClean[fill]))
    type2OverTimeClean[fill]=ROOT.TH1F("type2OverTimeClean"+str(fill),labels2,len(type2ValueErrorClean[fill]),0,len(type2ValueErrorClean[fill]))
    LSBlockNames=type1ValueErrorClean[fill].keys()
    LSBlockNames.sort()
    iCount=1
    for LSBlock in LSBlockNames:
        type1OverTimeClean[fill].SetBinContent(iCount,type1ValueErrorClean[fill][LSBlock][0])
        type1OverTimeClean[fill].SetBinError(iCount,type1ValueErrorClean[fill][LSBlock][1])
        type2OverTimeClean[fill].SetBinContent(iCount,type2ValueErrorClean[fill][LSBlock][0])
        type2OverTimeClean[fill].SetBinError(iCount,type2ValueErrorClean[fill][LSBlock][1])
        iCount=iCount+1

        type1OverTimeClean["all"].SetBinContent(iCleanAll,type1ValueErrorClean[fill][LSBlock][0])
        type1OverTimeClean["all"].SetBinError(iCleanAll,type1ValueErrorClean[fill][LSBlock][1])
        type2OverTimeClean["all"].SetBinContent(iCleanAll,type2ValueErrorClean[fill][LSBlock][0])
        type2OverTimeClean["all"].SetBinError(iCleanAll,type2ValueErrorClean[fill][LSBlock][1])
        iCleanAll=iCleanAll+1


    can.Update()
    type1OverTime[fill].Draw()
    can.Update()
    type1OverTimeClean[fill].Draw()
    fitType="pol0"
    type1OverTimeClean[fill].Fit(fitType,"QS")
    fitResult1=type1OverTimeClean[fill].GetFunction(fitType)
    type2OverTimeClean[fill].Fit(fitType,"QS")
    fitResult2=type2OverTimeClean[fill].GetFunction(fitType)
    try:
        value1=fitResult1.GetParameter(0)
        error1=fitResult1.GetParError(0)
        value2=fitResult2.GetParameter(0)
        error2=fitResult2.GetParError(0)
        print fill,value1,error1,value2,error2
        if error1<0.003 and int(fill)>4220:
            tgraph1.SetPoint(iFill,float(fill),value1)
            tgraph1.SetPointError(iFill,0,error1)
            tgraph2.SetPoint(iFill,float(fill),value2)
            tgraph2.SetPointError(iFill,0,error2)
            iFill=iFill+1
            print "FILLING TGRAPHS",iFill
            if value1<-0.01:
                print "LARGE TYPE 1 OUTLIER"
        iCount=iCount+1
        csvSummary.write(str(fill)+","+str(fitResult1.GetParameter(0))+","+str(fitResult1.GetParError(0))+"\n")
    except:
        print fill,"giveup"

    can.Update()
    type2OverTime[fill].Draw()
    can.Update()
    type2OverTimeClean[fill].Draw()

can.SetTickx()
can.SetTicky()
text=ROOT.TLatex(0.72,0.92,"2016  (13TeV)")
text.SetNDC()
text.SetTextFont(62)
text.SetTextSize(0.05)
text2=ROOT.TLatex(0.15,0.92,"CMS #bf{#scale[0.75]{#it{Preliminary}}}")
text2.SetNDC()
text2.SetTextSize(0.05)
text2.SetTextFont(62)

type1OverTime["all"].Draw()
type1OverTimeClean["all"].Draw()
type2OverTime["all"].Draw()
type2OverTimeClean["all"].Draw()

tgraph1.GetYaxis().SetTitleOffset(1.0)
tgraph1.SetMarkerStyle(23)
tgraph1.SetMarkerSize(1)
tgraph1.SetMarkerColor(kBlue)
tgraph1.Draw("AP")
text.Draw("same")
text2.Draw("same")
can.Update()
can.SaveAs("type1_residualPerFill_"+args.label+".png")
can.SaveAs("type1_residualPerFill_"+args.label+".C")

tgraph2.GetYaxis().SetTitleOffset(1.3)
tgraph2.SetMarkerStyle(23)
tgraph2.SetMarkerSize(1)
tgraph2.SetMarkerColor(kBlue)
tgraph2.Draw("AP")
text.Draw("same")
text2.Draw("same")
can.Update()
can.SaveAs("type2_residualPerFill_"+args.label+".png")
can.SaveAs("type2_residualPerFill_"+args.label+".C")


tgraph1.Write()
tgraph2.Write()

oFile.Write()
oFile.Close()

