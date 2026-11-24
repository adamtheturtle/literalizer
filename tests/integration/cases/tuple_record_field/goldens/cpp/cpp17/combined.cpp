#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{
    {"call", "send"},
    {"args", std::vector<std::variant<int, std::string>>{1, "email", "a@gmail.com", 100}},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, std::vector<std::variant<int, std::string>>>>{
    {"call", "send"},
    {"args", std::vector<std::variant<int, std::string>>{1, "email", "a@gmail.com", 100}},
};
    (void)my_data;
    return 0;
}
