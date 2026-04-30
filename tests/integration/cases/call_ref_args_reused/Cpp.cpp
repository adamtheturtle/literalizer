#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<std::map<std::string, std::string>, int>>>{
    std::vector<std::variant<std::map<std::string, std::string>, int>>{std::map<std::string, std::string>{{"$ref", "repeated_var"}}, 1},
    std::vector<std::variant<std::map<std::string, std::string>, int>>{std::map<std::string, std::string>{{"$ref", "single_var"}}, 0},
    std::vector<std::variant<std::map<std::string, std::string>, int>>{std::map<std::string, std::string>{{"$ref", "repeated_var"}}, 8},
};
    (void)my_data;
    return 0;
}
