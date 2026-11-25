#include <array>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::array<std::map<std::string, std::array<int, 1>>, 1>, std::array<std::map<std::string, std::array<int, 2>>, 1>>>{
    {"a", std::array<std::map<std::string, std::array<int, 1>>, 1>{std::map<std::string, std::array<int, 1>>{{"item", std::array<int, 1>{1}}}}},
    {"b", std::array<std::map<std::string, std::array<int, 2>>, 1>{std::map<std::string, std::array<int, 2>>{{"item", std::array<int, 2>{2, 3}}}}},
};
    (void)my_data;
    return 0;
}
