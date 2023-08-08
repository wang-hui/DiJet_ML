ROOT::Math::PtEtaPhiMVector get_lvec(float Pt, float Eta, float Phi, float M) {
    ROOT::Math::PtEtaPhiMVector Lvec(Pt, Eta, Phi, M);
    return Lvec;
}

float get_y(float Pt1, float Eta1, float Phi1, float M1, float Pt2, float Eta2, float Phi2, float M2) {
    auto Lvec1 = get_lvec(Pt1, Eta1, Phi1, M1);
    auto Lvec2 = get_lvec(Pt2, Eta2, Phi2, M2);
    auto LvecSum = Lvec1 + Lvec2;

    return LvecSum.Rapidity();
}
