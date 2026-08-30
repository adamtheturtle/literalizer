#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto a = std::map<std::string, std::variant<std::string, int>>{
    {"k", "s"},
};
auto my_data = std::vector<std::map<std::string, std::variant<std::string, int>>>{
    std::move(a),
    std::map<std::string, std::variant<std::string, int>>{{"k", 1}},
};
    (void)my_data;
    return 0;
}
