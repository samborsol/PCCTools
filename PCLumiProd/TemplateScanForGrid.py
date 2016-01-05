import ROOT
import os
import subprocess
import argparse
import numpy
import time

parser=argparse.ArgumentParser()
#parser.add_argument("-h", "--help", help="Display this message.")
parser.add_argument("-a", default="0.076,0.077,0.1", help="Parameter a min,max,step.  Default:  0.076,0.077,0.1")
parser.add_argument("-b", default="0.0006,0.0009,0.00005", help="Parameter b min,max,step.  Default:  0.0006,0.0009,0.00005")
parser.add_argument("-c", default="0.012,0.02,0.0005", help="Parameter c min,max,step.  Default:  0.012,0.02,0.005")
parser.add_argument("-d", "--dir", default="JobDir", help="For output and jobs.  Default: JobDir")
parser.add_argument("--batch", default=False, help="Do jobs on lxbatch.  Default:  True")
args=parser.parse_args()

a=args.a.split(",")
alist=numpy.arange(float(a[0]),float(a[1]),float(a[2]))

b=args.b.split(",")
blist=numpy.arange(float(b[0]),float(b[1]),float(b[2]))

c=args.c.split(",")
clist=numpy.arange(float(c[0]),float(c[1]),float(c[2]))

if not os.path.isdir(args.dir):
    os.makedirs(args.dir)

maxJobs=5
cmds=[]
for ia in alist:
    for ib in blist:
        for ic in clist:
            label="a"+str(ia)+"_b"+str(ib)+"_c"+str(ic)
            cmd=["python","DerivePCCCorrections.py","-f","Randoms_251496_251643_254833.root","-r","251496,251643","-l",label,"-p",str(ia)+","+str(ib)+","+str(ic),"-b"]
            if args.batch:
                cmd=["python","../DerivePCCCorrections.py","-f","../Randoms_251496_251643_254833.root","-r","251496,251643,254833","-l",label,"-p",str(ia)+","+str(ib)+","+str(ic),"-b"]
                baseName="job_"+label
                jobFileName=args.dir+"/"+baseName+".sh"
                jobFile=open(jobFileName,"a+")
                jobFile.write("cd "+os.getcwd()+"/"+args.dir+"\n")
                for part in cmd:
                    jobFile.write(part+" ")
                jobFile.write("\n")
                jobFile.close()
                cmd="bsub -q 8nh -J "+label+" -o "+baseName+".log < "+jobFileName
       
            cmds.append(cmd)
icmd=0
iSleep=0
print len(cmds),"total jobs"
while icmd!=len(cmds):
    out=[line for line in subprocess.check_output(["ps"]).split("\n") if line.find("DerivePCCCorrections.py") !=-1 ]
    if len(out) < maxJobs:
        if args.batch:
            os.system(cmds[icmd])
        else:
            subprocess.Popen(cmds[icmd])
        icmd=icmd+1
    else:
        print "Waiting 60 seconds",iSleep,icmd,"of",len(cmds)
        iSleep=iSleep+1
        time.sleep(60)
            


##usage: DerivePCCCorrections.py [-h] [-f FILE] [-d DIR] [-r RUNS] [--auto]
##                               [-l LABEL] [-a ALL] [--noType1] [--noType2]
##                               [-u] [-b] [-p PAR]
##
##optional arguments:
##  -h, --help            show this help message and exit
##  -f FILE, --file FILE  The path to a cert tree.
##  -d DIR, --dir DIR     The path to a directory of cert trees.
##  -r RUNS, --runs RUNS  Comma separated list of runs.
##  --auto                Determine the runs from the certtree
##  -l LABEL, --label LABEL
##                        The label for outputs
##  -a ALL, --all ALL     Apply both the type1 and type2 correction
##  --noType1             Only apply the type2 correction
##  --noType2             Only apply the type1 correction
##  -u, --useresponse     Use the final response instead of the real activity to
##                        calculate the Type2 Correction
##  -b, --batch           Batch mode (doesn't make GUI TCanvases)
##  -p PAR, --par PAR     The parameters for type1 and type2 correction
