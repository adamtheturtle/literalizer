#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::string>>>{
    {"left", std::vector<std::variant<int, std::string>>{1, "one"}},
    {"right", std::vector<std::variant<int, std::string>>{2, "two"}},
};
    (void)my_data;
    return 0;
}
