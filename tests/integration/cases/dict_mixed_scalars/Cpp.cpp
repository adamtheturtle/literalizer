#include <initializer_list>
#include <string>
#include <map>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<int, std::string>>{
    {"a", 1},
    {"b", "x"},
};
    (void)my_data;
}
