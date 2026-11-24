#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<int>>>{
    {"name", "Alice"},
    {"scores", std::vector<int>{
        10,
        20,
        30,
    }},
};
    (void)my_data;
    return 0;
}
