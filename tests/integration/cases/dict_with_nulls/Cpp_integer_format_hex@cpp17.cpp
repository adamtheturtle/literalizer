#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::nullptr_t, int>>{
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 0x1e},
};
    (void)my_data;
    return 0;
}
