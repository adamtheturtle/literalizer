#include <initializer_list>
#include <string>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = {
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
}
