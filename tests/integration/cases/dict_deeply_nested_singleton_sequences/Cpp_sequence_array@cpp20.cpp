#include <initializer_list>
#include <string>
#include <map>
#include <array>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::vector<std::vector<int>>>>>{
    {"deep", {{{std::array<int, 1>{1}}}}},
};
    (void)my_data;
    return 0;
}
