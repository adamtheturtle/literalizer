#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto foo = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::map<std::string, std::variant<std::map<std::string, std::map<std::string, std::string>>, std::vector<std::map<std::string, std::variant<int, std::string>>>>>{
    {"mapping", std::map<std::string, std::map<std::string, std::string>>{{"value", std::move(foo)}}},
    {"items", std::vector<std::map<std::string, int>>{std::map<std::string, std::variant<int, std::string>>{{"other", 1}}, std::move(foo)}},
};
    (void)my_data;
    return 0;
}
