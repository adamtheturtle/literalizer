#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, int>>>{
    std::map<std::string, std::variant<std::string, int>>{
        {"key", "hello   world"},
        {"value", 1},
    },
};
    (void)my_data;
    return 0;
}
