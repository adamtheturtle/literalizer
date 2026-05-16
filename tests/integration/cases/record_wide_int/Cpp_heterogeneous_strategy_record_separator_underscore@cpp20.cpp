#include <initializer_list>
#include <string>
#include <map>
#include <variant>
struct Record0 { int quantity{}; unsigned long long big{}; double ratio{}; std::string label; bool ok{}; };
int main() {
auto my_data = Record0{
    .quantity = 1'000'000,
    .big = 18446744073709551615ULL,
    .ratio = 2.5,
    .label = "tag",
    .ok = true,
};
    (void)my_data;
    return 0;
}
