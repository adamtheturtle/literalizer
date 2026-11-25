#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string>>>{
    std::map<std::string, std::variant<int, std::string>>{{"first", 1}},
    std::map<std::string, std::variant<int, std::string>>{{"repeated", "a"}},
    std::map<std::string, std::variant<int, std::string>>{{"repeated", "b"}},
};
    (void)my_data;
    return 0;
}
