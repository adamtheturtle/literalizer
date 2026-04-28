#include <initializer_list>
#include <string>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::variant<int, std::string>>{
    {"a", 1},
    {"b", "x"},
};
    (void)my_data;
    return 0;
}
