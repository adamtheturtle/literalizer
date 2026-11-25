#include <array>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::array<std::map<std::string, std::array<long long, 1>>, 1>, std::array<std::map<std::string, std::array<long long, 2>>, 1>>>{
    {"positive", std::array<std::map<std::string, std::array<long long, 1>>, 1>{std::map<std::string, std::array<long long, 1>>{{"item", std::array<long long, 1>{2147483648}}}}},
    {"negative", std::array<std::map<std::string, std::array<long long, 1>>, 1>{std::map<std::string, std::array<long long, 1>>{{"item", std::array<long long, 1>{-2147483649}}}}},
    {"mixed", std::array<std::map<std::string, std::array<long long, 2>>, 1>{std::map<std::string, std::array<long long, 2>>{{"item", std::array<long long, 2>{0, 2147483648}}}}},
};
    (void)my_data;
    return 0;
}
