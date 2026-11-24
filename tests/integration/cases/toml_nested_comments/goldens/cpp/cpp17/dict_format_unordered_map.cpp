#include <string>
#include <unordered_map>
#include <variant>
#include <vector>
int main() {
auto my_data = std::unordered_map<std::string, std::variant<std::unordered_map<std::string, int>, int, std::vector<std::unordered_map<std::string, std::string>>>>{
    // About the first dotted key.
    // About the second dotted key.
    {"dotted", std::unordered_map<std::string, int>{{"first", 1}, {"second", 2}}},
    {"plain", 3},  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    {"entries", std::vector<std::unordered_map<std::string, std::string>>{std::unordered_map<std::string, std::string>{{"name", "one"}}, std::unordered_map<std::string, std::string>{{"name", "two"}}}},
    // Inside the table.
    {"table", std::unordered_map<std::string, int>{{"inner", 4}}},
};
    (void)my_data;
    return 0;
}
