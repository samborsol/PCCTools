import ROOT
import sys,os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Find a ROOT file among many with the run number you input.')
parser.add_argument('-f', '--filename', type=str, default="", help='A file to be checked.')
parser.add_argument('-d', '--directory',type=str, default="", help='A directory containing root files to be checked.')
parser.add_argument('-t', '--treename', type=str, default="lumi/tree", help="Tree name (default:  lumi/tree")
parser.add_argument('-r', '--run', type=str, default="", help="Run to search for")
parser.add_argument('-l', '--ls',  type=str, default="", help="LS to search for")
args = parser.parse_args()

if args.filename=="" and args.directory=="":
    print "Re-run giving '-f FILENAME' or '-d DIRECTORY' as an agrument"
    sys.exit(1)



def CheckFile(file):
    tfile=ROOT.TFile.Open(file)
    ttree=tfile.Get(args.treename)

    searchRunLS=""
    if args.run!="":
        searchRunLS="run=="+args.run
        if args.ls!="":
            searchRunLS=searchRunLS+"&&LS=="+args.ls
    elif args.ls!="":
        searchRunLS="LS=="+args.ls
    else:
        print "Nothing to search for (run,ls): ("+args.run+","+args.ls+")"
        sys.exit(-1)


    try:
        return ttree.GetEntries(searchRunLS)
    except:
        print "Failed to GetEntries for",file
        return -1
    

def GetFileList(dir):
    filenames=[]
    if dir.find("/store")==0:
        fileinfos=subprocess.check_output(["cmsLs", dir])
        fileinfos=fileinfos.split("\n")

        for fileinfo in fileinfos:
            info=fileinfo.split()
            if len(info)<4:
                continue
            filename=info[4]
            if filename.find(".root") == -1:
                continue
            filenames.append("root://eoscms//eos/cms"+filename)

    else:
        try:
            files=os.listdir(dir)
            for file in files:
                if file.find(".root")==-1:
                    continue
                filenames.append(dir+"/"+file)
        except:
            print "Can't listdir on",dir
    return filenames




if args.filename!="":
    num=CheckFile(args.filename)
    if num>0:
        print args.filename,"has",num

if args.directory!="":
    files=GetFileList(args.directory)

    print "files containing run",args.run,"ls",args.ls
    for file in files:
        num=CheckFile(file)
        if num>0:
            print file#,"has",num
