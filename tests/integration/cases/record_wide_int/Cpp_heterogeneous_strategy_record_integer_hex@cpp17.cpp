#include <initializer_list>
#include <string>
#include <variant>
struct Record0 { int quantity{}; unsigned long long big{}; double ratio{}; std::string label; bool ok{}; };
int main() {
auto my_data = Record0{
    0xf4240,
    18446744073709551615ULL,
    2.5,
    "tag",
    true,
};
    (void)my_data;
    return 0;
}
