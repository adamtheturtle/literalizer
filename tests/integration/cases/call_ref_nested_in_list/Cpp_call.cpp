#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
auto my_other = 7;
process(std::vector<std::variant<std::map<std::string, std::string>, int, std::string>>{std::map<std::string, std::string>{{"ref", "my_var"}}, 42, "static"});
process(std::vector<std::variant<std::map<std::string, std::string>, int, std::string>>{std::map<std::string, std::string>{{"ref", "my_other"}}, 7, "label"});
    return 0;
}
