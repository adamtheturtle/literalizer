#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{
    {"call", "send"},
    {"args", std::vector<std::variant<int, std::string>>{1, "email"}},
};
    (void)my_data;
    return 0;
}
