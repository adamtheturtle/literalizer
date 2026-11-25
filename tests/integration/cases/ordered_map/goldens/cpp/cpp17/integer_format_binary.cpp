#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::string, int, bool>>>{
    {"name", "Alice"},
    {"age", 0b11110},
    {"active", true},
};
    (void)my_data;
    return 0;
}
