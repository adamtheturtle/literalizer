#include <string>
#include <utility>
#include <vector>
struct Record0 { int replacement{}; int present{}; };
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<Record0>>>{
    {"rows", std::vector{Record0{-1, 1}, Record0{2, 3}}},
};
    (void)my_data;
    return 0;
}
