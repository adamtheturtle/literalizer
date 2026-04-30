#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, int>>>{
    std::map<std::string, std::variant<std::string, int>>{{"name", "Alice"}, {"age", 30}},
    std::map<std::string, std::variant<std::string, int>>{{"name", "Bob"}, {"age", 25}},
};
    (void)my_data;
    return 0;
}
