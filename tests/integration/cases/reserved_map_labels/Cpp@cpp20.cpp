#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, int>{
    {"if", 1},
    {"then", 2},
    {"else", 3},
    {"let", 4},
    {"in", 5},
    {"using", 6},
    {"missing", 7},
    {"assert", 8},
    {"as", 9},
    {"Infinity", 10},
    {"NaN", 11},
    {"merge", 12},
    {"Some", 13},
    {"toMap", 14},
    {"forall", 15},
    {"with", 16},
    {"ordinary", 17},
};
    (void)my_data;
    return 0;
}
