#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<std::string>>>>{
    {"alpha", std::vector<std::variant<int, std::vector<std::string>>>{2, std::vector<std::string>{}}},
    {"beta", std::vector<std::variant<int, std::vector<std::string>>>{5, std::vector<std::string>{"x"}}},
};
    (void)my_data;
    return 0;
}
