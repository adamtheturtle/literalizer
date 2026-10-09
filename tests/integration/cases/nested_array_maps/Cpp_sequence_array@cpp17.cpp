#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::array<std::array<std::map<std::string, int>, 1>, 2>>{
    {"groups", std::array<std::array<std::map<std::string, int>, 1>, 2>{std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"id", 1}}}, std::array<std::map<std::string, int>, 1>{std::map<std::string, int>{{"id", 2}}}}},
};
    (void)my_data;
    return 0;
}
