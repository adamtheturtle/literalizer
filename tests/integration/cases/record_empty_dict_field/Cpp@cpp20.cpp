#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, std::nullptr_t>, int>>{
    {"f", std::map<std::string, std::nullptr_t>{}},
    {"g", 1},
};
    (void)my_data;
    return 0;
}
