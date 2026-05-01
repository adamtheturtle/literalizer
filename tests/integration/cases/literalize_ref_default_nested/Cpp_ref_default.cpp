#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_var = std::map<std::string, std::string>{
    {"_", "_"},
};
auto item_var = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::map<std::string, std::variant<std::map<std::string, std::string>, std::vector<std::map<std::string, std::string>>>>{
    {"key", std::move(my_var)},
    {"items", std::vector<std::map<std::string, std::string>>{std::move(item_var), std::map<std::string, std::string>{{"fallback", "value"}}}},
};
    (void)my_data;
    return 0;
}
