#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{
        /* indented */
        {"x", 1},
    }},
    {"b", 2},
};
    (void)my_data;
    return 0;
}
