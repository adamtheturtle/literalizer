#include <array>
#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::array<std::map<std::string, std::array<int, 1>>, 1>>{
    {"a", std::array<std::map<std::string, std::array<int, 1>>, 1>{std::map<std::string, std::array<int, 1>>{{"item", std::array<int, 1>{1}}}}},
    {"b", std::array<std::map<std::string, std::array<int, 1>>, 1>{std::map<std::string, std::array<int, 1>>{{"item", std::array<int, 1>{2}}}}},
};
    (void)my_data;
    return 0;
}
