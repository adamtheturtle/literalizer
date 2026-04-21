#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>>{
    {"users", std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>{std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
my_data = std::map<std::string, std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>>{
    {"users", std::vector<std::map<std::string, std::variant<std::string, std::vector<std::string>>>>{std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
