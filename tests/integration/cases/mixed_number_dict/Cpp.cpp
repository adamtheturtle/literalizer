#include <initializer_list>
#include <string>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
}
