## PCCTools
####Checkout instructions on lxplus:  
cmsrel CMSSW_7_6_1  
cd CMSSW_7_6_1/src/  
cmsenv  
  
  
####Basic Git Instructions

0. Create your own fork of CMS-LUMI-POG/PCCTools (upper right)
1. Check out the group's version of the tools (easiest way to keep in sync)
  a) git clone https://github.com/CMS-LUMI-POG/PCCTools
2. Make a remote to your fork  
  a) git remote add YOURGITUSERNAME http://github.com/YOURGITUSERNAME/DataCert
3. Check in your edited files  
  a) git add file1 file2  
  b) git commit -m "file1 and file2 are changed because..."  
4. push to YOUR fork in a BRANCH
  a) git checkout -b update-whatiam-date  
  b) git push YOURGITUSERNAME update-whatiam-date
5. Make a pull request (PR) with your changes update-newcurrents-data  
  a) at https://github.com/CMS-LUMI-POG/PCCTools  
  b) let someone review and merge into the "master"
6. Keep your master in syne with CMS-LUMI-POG/PCCTools's master  
  a) git checkout master  
  b) git push YOURGITUSERNAME master
  
  
####Instructions for producing PCC ntuples:

cmsrel CMSSW_7_6_X  
cd CMSSW_7_6_X/src  
cmsenv  
git cms-addpkg RecoLuminosity/LumiProducer  
scram b -j 8  
cd RecoLuminosity/LumiProducer/test/analysis/test  

The script Run_PixVertex_LS.py can generate the PCC ntuples for data certification and other purposes.  
The script crab3_dataCert_ZeroBiasSkim_150924.py can be modified to submit the CRAB jobs.

In the CRAB configuration file, "config.Data.runRange" should be the run numbers to be certified; "config.Data.inputDataset" can be fetched by " das_client --query='dataset dataset=/ZeroBias\*/Run2015\*Lumi\*/ALCARECO run=RUN_NUMBER' " 


To submit CRAB jobs:  
crab submit -c crab3_dataCert_ZeroBiasSkim_150924.py
