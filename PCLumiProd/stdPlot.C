#include <TH1F.h>
#include <TCanvas.h>
#include <TFile.h>

void stdPlot(std::string baseName, TFile* file){
    std::vector< std::string > histNames;
    histNames.clear();
    histNames.push_back(std::string("Before_Corr_"));
    histNames.push_back(std::string("After_TypeI_Corr_"));
    histNames.push_back(std::string("After_TypeI_TypeII_Corr_"));
    histNames.push_back(std::string("After_Corr_"));

    for(int iHist=0; iHist<histNames.size(); iHist++){
        histNames[iHist].append(baseName);
        //std::cout<<iHist<<" name "<<histNames[iHist]<<std::endl;
    }

    std::vector< TH1F* > hists;
    hists.clear();
    for(int iHist=0; iHist<histNames.size(); iHist++){
        hists.push_back((TH1F*)file->Get(histNames[iHist].c_str()));
        //hists[iHist]=(TH1F*) hists[iHist]->Clone();
    }

    int colors[] = {600, 416, 632, 1};
    int styles[] = {24, 25, 26, 27};
    
    TCanvas * can = new TCanvas(baseName.c_str(),"",700,700);
    for(int iHist=0; iHist<histNames.size(); iHist++){
        hists[iHist]->SetMarkerColor(colors[iHist]);
        hists[iHist]->SetMarkerStyle(styles[iHist]);
        if(iHist==0){
            hists[iHist]->Draw("p");
        } else {
            hists[iHist]->Draw("psame");
        }
    } 

    can->Update();

    std::string junk;
    cin>>junk;

    hists[0]->GetYaxis()->SetRangeUser(-0.01,0.3);
    can->Update();
}
