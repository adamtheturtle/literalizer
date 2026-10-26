#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<std::string>>>>{
    {"test", std::vector<std::variant<int, std::vector<std::string>>>{5, std::vector<std::string>{"compile", "test"}}},
    {"package", std::vector<std::variant<int, std::vector<std::string>>>{7, std::vector<std::string>{"link", "test"}}},
};
    (void)my_data;
    return 0;
}
