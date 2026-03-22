#include <string>
#include <map>
#include <vector>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    {"users", {{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
