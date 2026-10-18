#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::array<long long, 2>>{
    {"a", std::array<long long, 2>{4294967296, 4294967297}},
};
    (void)my_data;
    return 0;
}
