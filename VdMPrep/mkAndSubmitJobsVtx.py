import ROOT
import sys,os
import argparse
import math
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument("-p",  "--path",  help="EOS path to PCCNTuples... /store/user/..")
parser.add_argument("-d",  "--dir", default="JobsDir", help="Output directory")
parser.add_argument("-de",  "--direos", default="", help="Output Eos directory")
parser.add_argument('--label', type=str, default="", help="Label for output file")
parser.add_argument('--mintime', type=float, default=0, help="Minimum time stamp")
parser.add_argument('--maxtime', type=float, default=math.pow(2,66), help="Maximum time stamp")
parser.add_argument("-s",  "--sub", action='store_true', default=False, help="bsub created jobs")
parser.add_argument('--vetoModules', type=str, default="vetoModules.txt", help="Text file containing list of pixel modules to veto (default: ../vetoModules.txt)")

args=parser.parse_args()


def MakeJob(outputdir,jobid,filename,mintime,maxtime):
    joblines=[]
    joblines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh")
    joblines.append("cd "+outputdir)
    joblines.append("cmsenv")
    #joblines.append("eval `scramv1 runtime -sh`")
    joblines.append("python ../makeVdMMiniTreeVtx.py --pccfile="+args.path+filename+" --label="+args.label+"_"+str(jobid)+" --mintime="+str(mintime)+" --maxtime="+str(maxtime)+" --vetoModules=../"+args.vetoModules)
    joblines.append("cmsStage *.root "+args.direos)
    scriptFile=open(outputdir+"/job_"+str(jobid)+".sh","w+")
    for line in joblines:
        scriptFile.write(line+"\n")
        
    scriptFile.close()

def SubmitJob(job,queue="8nh"):
    baseName=str(job.split(".")[0])
    cmd="bsub -q "+queue+" -J "+baseName.split("/")[1]+" -o "+baseName+".log < "+str(job)
    output=os.system(cmd)
    if output!=0:
        print job,"did not submit properly"
        print cmd


# ls the eos directory
fileinfos=subprocess.check_output(["cmsLs", args.path])
fileinfos=fileinfos.split("\n")
print fileinfos

filenames={}
for fileinfo in fileinfos:
    info=fileinfo.split()
    #if len(info)<4:
    #    continue
    filename=fileinfo
    if filename.find(".root") == -1:
        continue
    jobid=filename.split("/")[-1].split(".")[0].split("_")[-1]
    #print jobid, filename
    filenames[int(jobid)]=filename

print filenames

fullOutPath=os.getcwd()
if not os.path.exists(args.dir):
    os.makedirs(args.dir)
fullOutPath=fullOutPath+"/"+args.dir

for job in filenames:
    MakeJob(fullOutPath,job,filenames[job],args.mintime,args.maxtime)

if args.sub:
    print "Submitting",len(filenames),"jobs"
    for job in filenames:
        SubmitJob(args.dir+"/job_"+str(job)+".sh")
