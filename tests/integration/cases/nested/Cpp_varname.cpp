#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void _check() {
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
_Any my_data = {
    {"users", {{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
