#include <array>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::array<long long, 2>>{
    {"a", std::array<long long, 2>{4294967296, 4294967297}},
};
    (void)my_data;
    return 0;
}
