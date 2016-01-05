#!/bin/csh

#input=$1
#a=$2
#b=$3
#c=$4
#lable=$5
#script=$6

source /cvmfs/cms.cern.ch/cmsset_default.csh
setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc472/lcg/root/5.32.00-cms
setenv PATH $ROOTSYS/bin:$PATH
set current=`pwd`
echo $current
#cd /uscms/home/jluo/CMSSW/CMSSW_7_4_3/src
#cmsenv
scram p CMSSW CMSSW_7_4_3
cd CMSSW_7_4_3
cmsenv
cd $current

python $6 -f $1 -p $2,$3,$4 -r 251496,251643 -l $5 -b
