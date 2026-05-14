#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::variant<int, std::string, std::vector<std::string>>>>{
    {"user", std::map<std::string, std::variant<int, std::string>>{{"id", 1}, {"name", "Alice"}}},
    {"project", std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"title", "report"}, {"tags", std::vector<std::string>{"draft", "urgent"}}}},
};
(void)my_data;
my_data = std::map<std::string, std::map<std::string, std::variant<int, std::string, std::vector<std::string>>>>{
    {"user", std::map<std::string, std::variant<int, std::string>>{{"id", 1}, {"name", "Alice"}}},
    {"project", std::map<std::string, std::variant<std::string, std::vector<std::string>>>{{"title", "report"}, {"tags", std::vector<std::string>{"draft", "urgent"}}}},
};
    (void)my_data;
    return 0;
}
