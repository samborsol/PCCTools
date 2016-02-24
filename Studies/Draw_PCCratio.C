void Draw_PCCratio(){

    gStyle->SetOptStat(0);

    TCanvas *c = new TCanvas("c", "c", 800, 500);
    c->cd();
    c->SetTickx();
    c->SetTicky();
    

    TFile *f = new TFile("Overall.root");

    TH1F *h_PCC_layer_0 = (TH1F*)f->Get("h_PCC_Layer_1");
    TH1F *h_PCC_layer_1 = (TH1F*)f->Get("h_PCC_Layer_2");
    TH1F *h_PCC_layer_2 = (TH1F*)f->Get("h_PCC_Layer_3");
    TH1F *h_PCC_layer_3 = (TH1F*)f->Get("h_PCC_Layer_4");
    TH1F *h_PCC_total = (TH1F*)f->Get("h_PCC_total");

    TH1F *ratio_0 = (TH1F*)h_PCC_layer_0->Clone();
    TH1F *ratio_1 = (TH1F*)h_PCC_layer_1->Clone();
    TH1F *ratio_2 = (TH1F*)h_PCC_layer_2->Clone();
    TH1F *ratio_3 = (TH1F*)h_PCC_layer_3->Clone();

    ratio_0->Divide(h_PCC_total);
    ratio_1->Divide(h_PCC_total);
    ratio_2->Divide(h_PCC_total);
    ratio_3->Divide(h_PCC_total);

    for(int i=0; i<ratio_0->GetNbinsX(); i++){
        ratio_0->SetBinError(i, 0.00001);

    }

    for(int j=0; j<ratio_1->GetNbinsX(); j++){
        ratio_1->SetBinError(j, 0.00001);

    }

    for(int k=0; k<ratio_2->GetNbinsX(); k++){
        ratio_2->SetBinError(k, 0.00001);

    } 

    for(int l=0; l<ratio_3->GetNbinsX(); l++){
        ratio_3->SetBinError(l, 0.00001);

    }

    ratio_0->SetTitle("");

    ratio_0->SetMarkerStyle(23);
    ratio_1->SetMarkerStyle(23);
    ratio_2->SetMarkerStyle(23);
    ratio_3->SetMarkerStyle(23);

    ratio_0->SetMarkerColor(kBlue);
    ratio_1->SetMarkerColor(kRed);
    ratio_2->SetMarkerColor(kGreen);
    ratio_3->SetMarkerColor(6);

    ratio_0->SetLineColor(kBlue);
    ratio_1->SetLineColor(kRed);
    ratio_2->SetLineColor(kGreen);
    ratio_3->SetLineColor(6);

  //  ratio_0->SetLineWidth(4);
  //  ratio_1->SetLineWidth(4);
  //  ratio_2->SetLineWidth(4);
  //  ratio_3->SetLineWidth(4);

    ratio_0->GetXaxis()->SetTitle("Date (Day/Month)");
    ratio_0->GetXaxis()->SetTimeDisplay(1);
    //ratio_0->GetXaxis()->SetTimeOffset("GMT");
    ratio_0->GetXaxis()->SetNdivisions(-503);
    ratio_0->GetXaxis()->SetTimeFormat("  %d/%m %F1970-01-01 00:00:00");
    ratio_0->GetYaxis()->SetTitle("Relative Contribution");
    //ratio_0->GetXaxis()->SetRangeUser(251000, 261000);
    ratio_0->GetYaxis()->SetRangeUser(0.17,0.35);
    ratio_0->Draw("PE");
    ratio_1->Draw("PE SAME");
    ratio_2->Draw("PE SAME");
    ratio_3->Draw("PE SAME");

    TLegend *len = new TLegend(0.5, 0.4, 0.85, 0.55);
    len->SetFillColor(0);
    len->SetLineColor(0);
    len->AddEntry(ratio_0,"barrel layer 2", "P");
    len->AddEntry(ratio_1,"barrel layer 3", "P");
    len->AddEntry(ratio_2,"forward disk 1", "P");
    len->AddEntry(ratio_3,"forward disk 2", "P");


    len->Draw("SAME");

    TLatex *text=new TLatex(0.72,0.85,"2015  (13TeV)");
    text->SetNDC();
    text->SetTextFont(62);
    text->SetTextSize(0.05);
    TLatex *text2=new TLatex(0.15,0.85,"CMS #bf{#scale[0.75]{#it{Preliminary}}}");
    text2->SetNDC();
    text2->SetTextSize(0.05);
    text2->SetTextFont(62);
    text->Draw("same");
    text2->Draw("same");
    c->SaveAs("new_PCC_stability.eps");
    c->SaveAs("new_PCC_stability.png");
}
