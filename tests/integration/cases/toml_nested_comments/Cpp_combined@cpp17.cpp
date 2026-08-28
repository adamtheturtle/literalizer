#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, int, std::vector<std::map<std::string, std::string>>>>{
    // About the first dotted key.
    // About the second dotted key.
    {"dotted", std::map<std::string, int>{{"first", 1}, {"second", 2}}},
    {"plain", 3},  // About the plain key.
    // Inside the table.
    {"table", std::map<std::string, int>{{"inner", 4}}},
    // Before the first entry.
    // Before the second entry.
    {"entries", std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "one"}}, std::map<std::string, std::string>{{"name", "two"}}}},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::map<std::string, int>, int, std::vector<std::map<std::string, std::string>>>>{
    // About the first dotted key.
    // About the second dotted key.
    {"dotted", std::map<std::string, int>{{"first", 1}, {"second", 2}}},
    {"plain", 3},  // About the plain key.
    // Inside the table.
    {"table", std::map<std::string, int>{{"inner", 4}}},
    // Before the first entry.
    // Before the second entry.
    {"entries", std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "one"}}, std::map<std::string, std::string>{{"name", "two"}}}},
};
    (void)my_data;
    return 0;
}
