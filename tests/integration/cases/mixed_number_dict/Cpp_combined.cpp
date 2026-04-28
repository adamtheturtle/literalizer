#include <initializer_list>
#include <string>
#include <map>
auto main() -> int {
auto my_data = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
(void)my_data;
my_data = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
    (void)my_data;
    return 0;
}
