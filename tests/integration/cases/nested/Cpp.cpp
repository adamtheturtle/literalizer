#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
const auto my_data = std::map<std::string, std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>>{
    {"users", std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>{std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
    (void)my_data;
    return 0;
}
