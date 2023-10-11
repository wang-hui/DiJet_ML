typedef ROOT::Math::PtEtaPhiMVector lvec;
typedef std::pair<lvec, lvec> lvecPair;

std::pair<lvecPair, lvecPair> make_dijet_pair (const lvec & J1, const lvec & J2, const lvec & J3, const lvec & J4) {
    auto Dijet1 = std::make_pair(J1, J2);
    auto Dijet2 = std::make_pair(J3, J4);

    if ((J1+J2).M() > (J3+J4).M()) return std::make_pair(Dijet1, Dijet2);
    else return std::make_pair(Dijet2, Dijet1);
}

bool bigger_mass (const std::pair<lvecPair, lvecPair> & Pair1, const std::pair<lvecPair, lvecPair> & Pair2) {
    return (Pair1.first.first + Pair1.first.second).M() > (Pair2.first.first + Pair2.first.second).M();
}

std::vector<lvec> sort_dijet_mass (const lvec & J1, const lvec & J2, const lvec & J3, const lvec & J4) {
    auto Pair1 = make_dijet_pair(J1, J2, J3, J4);
    auto Pair2 = make_dijet_pair(J1, J3, J2, J4);
    auto Pair3 = make_dijet_pair(J1, J4, J2, J3);
    std::vector<std::pair<lvecPair, lvecPair>> VecOfPairOfPair = {Pair1, Pair2, Pair3};
    std::sort(VecOfPairOfPair.begin(), VecOfPairOfPair.end(), bigger_mass);
    std::vector<lvec> SortedJets;
    for(int i = 0; i < 3; i++) {
        SortedJets.push_back(VecOfPairOfPair.at(i).first.first);
        SortedJets.push_back(VecOfPairOfPair.at(i).first.second);
        SortedJets.push_back(VecOfPairOfPair.at(i).second.first);
        SortedJets.push_back(VecOfPairOfPair.at(i).second.second);
    }
    return SortedJets;
}

int min_index (float a, float b, float c) {
    std::vector<float> Input = {a, b, c};
    auto Iter = std::min_element(Input.begin(), Input.end());
    return std::distance(Input.begin(), Iter);
}

std::pair<int, float> max_index_val (float a, float b, float c) {
    std::vector<float> Input = {a, b, c};
    auto Iter = std::max_element(Input.begin(), Input.end());
    int Index = std::distance(Input.begin(), Iter);
    float Val = Input.at(Index);
    return std::make_pair(Index, Val);
}

template <typename T>
T col_index (T a, T b, T c, int index) {
    std::vector<T> Input = {a, b, c};
    return Input.at(index);
}

template <typename T>
std::vector<T> to_vec (T a, T b, T c, T d) {
    std::vector<T> Input = {a, b, c, d};
    return Input;
}

