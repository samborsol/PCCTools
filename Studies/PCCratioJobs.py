import ROOT
import sys
import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="EOS path to certtree files")
parser.add_argument("-d", "--dir", default="JobDir", help="Output Directory")
parser.add_argument("-o", "--outPath", default="", help="Specify the path of output files")
parser.add_argument("-j", "--json", default="", help="JSON file fo run/LSs to filter")
parser.add_argument("-s", "--sub", default=False, action="store_true", help="bsub created jobs")

args=parser.parse_args()

def MakeJob(outputdir, jobid, filename):

    joblines=[]
    joblines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh")
    joblines.append("cd "+outputdir)
    joblines.append("cmsenv")
    makeDataCMD ="python ../PCCstability.py --certfile="+args.path+"/"+filename
    if args.json!="":
        makeDataCMD=makeDataCMD+" --json="+args.json

    if args.outPath!="":
        makeDataCMD=makeDataCMD+" --output="+args.outPath

    makeDataCMD=makeDataCMD+" --label="+str(jobid)

    joblines.append(makeDataCMD)

    scriptFile=open(outputdir+"/job_"+str(jobid)+".sh", "w+")
    for line in joblines:
        scriptFile.write(line+"\n")

    scriptFile.close()

def SubmitJob(job, queue="1nh"):
    baseName=str(job.split(".")[0])
    cmd="bsub -q "+queue+" -J "+baseName+" -o "+baseName+".log < "+str(job)
    output=os.system(cmd)
    if output!=0:
        print job, "did not submit properly"
        print cmd


fileinfos=subprocess.check_output(["/afs/cern.ch/project/eos/installation/0.3.4/bin/eos.select","ls", args.path])
fileinfos=fileinfos.split("\n")

filenames={}
for fileinfo in fileinfos:

    filename=fileinfo
    if filename.find(".root") == -1:
        continue
    jobid=filename.split("/")[-1].split(".")[0].split("_")[-1]
    
    filenames[int(jobid)]=filename

fullOutPath = os.getcwd()
if not os.path.exists(args.dir):

    os.makedirs(args.dir)
fullOutPath=fullOutPath+"/"+args.dir

for job in filenames:
    MakeJob(fullOutPath, job, filenames[job])

if args.sub: 
    print "Submitting", len(filename), "jobs"

    for job in filenames:

        SubmitJob(args.dir+"/job_"+str(job)+".sh", "1nh")
