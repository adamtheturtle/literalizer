#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::vector<std::variant<int, std::map<std::string, int>>>>>{
    {"first", std::map<std::string, std::vector<std::variant<int, std::map<std::string, int>>>>{{"items", std::vector<std::variant<int, std::map<std::string, int>>>{1, std::map<std::string, int>{{"value", 2}}}}}},
    {"second", std::map<std::string, std::vector<std::variant<int, std::map<std::string, int>>>>{{"items", std::vector<std::variant<int, std::map<std::string, int>>>{1, std::map<std::string, int>{{"value", 3}}}}}},
};
    (void)my_data;
    return 0;
}
