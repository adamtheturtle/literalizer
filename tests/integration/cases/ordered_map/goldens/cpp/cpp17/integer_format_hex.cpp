#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::string, int, bool>>>{
    {"name", "Alice"},
    {"age", 0x1e},
    {"active", true},
};
    (void)my_data;
    return 0;
}
