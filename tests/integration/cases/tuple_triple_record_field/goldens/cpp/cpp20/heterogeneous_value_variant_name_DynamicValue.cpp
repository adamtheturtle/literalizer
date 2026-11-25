#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string, bool>>>>{
    {"call", "send"},
    {"args", std::vector<std::variant<int, std::string, bool>>{1, "email", true}},
};
    (void)my_data;
    return 0;
}
