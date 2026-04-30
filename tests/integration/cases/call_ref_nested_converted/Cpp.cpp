#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::vector<std::variant<std::map<std::string, std::string>, int, std::string>>>>{
    std::vector<std::vector<std::variant<std::map<std::string, std::string>, int, std::string>>>{std::vector<std::variant<std::map<std::string, std::string>, int, std::string>>{std::map<std::string, std::string>{{"$ref", "myVar"}}, 42, "static"}},
};
    (void)my_data;
    return 0;
}
