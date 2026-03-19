#include <initializer_list>
#include <cstddef>
#include <map>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"users", {{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
my_data = {
    {"users", {{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
