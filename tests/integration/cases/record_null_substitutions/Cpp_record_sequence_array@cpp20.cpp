#include <string>
#include <utility>
#include <vector>
struct Record0 { int replacement{}; int present{}; };
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<Record0>>>{
    {"rows", std::vector{Record0{.replacement = -1, .present = 1}, Record0{.replacement = 2, .present = 3}}},
};
    (void)my_data;
    return 0;
}
