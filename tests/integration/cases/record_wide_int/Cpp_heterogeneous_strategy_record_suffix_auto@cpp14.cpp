#include <initializer_list>
#include <string>
struct Record0 { long quantity{}; unsigned long long big{}; double ratio{}; std::string label; bool ok{}; };
int main() {
auto my_data = Record0{
    1000000L,
    18446744073709551615ULL,
    2.5,
    "tag",
    true,
};
    (void)my_data;
    return 0;
}
