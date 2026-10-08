#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::unordered_map<std::string, std::variant<std::unordered_map<std::string, std::variant<std::string, bool>>, std::vector<std::unordered_map<std::string, std::variant<std::string, double>>>>>{
    {"owner", std::unordered_map<std::string, std::variant<std::string, bool>>{{"name", "Ada"}, {"active", false}}},
    {"members", std::vector<std::unordered_map<std::string, std::variant<std::string, double>>>{std::unordered_map<std::string, std::variant<std::string, double>>{{"name", "Ada"}, {"score", 1.5}}, std::unordered_map<std::string, std::variant<std::string, double>>{{"name", "Bob"}, {"score", 2.5}}}},
};
    (void)my_data;
    return 0;
}
