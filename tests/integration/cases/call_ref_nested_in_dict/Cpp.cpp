#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::map<std::string, std::variant<std::map<std::string, std::string>, int>>>>{
    std::vector<std::map<std::string, std::variant<std::map<std::string, std::string>, int>>>{std::map<std::string, std::variant<std::map<std::string, std::string>, int>>{{"key", std::map<std::string, std::string>{{"$ref", "my_var"}}}, {"count", 42}}},
};
    (void)my_data;
    return 0;
}
