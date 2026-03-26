#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::map<std::string, std::vector<std::map<std::string, _Any>>>{
    {"users", std::vector<std::map<std::string, _Any>>{{{"name", "Bob"}, {"tags", std::vector<std::string>{"admin", "user"}}}, {{"name", "Carol"}, {"tags", std::vector<std::string>{"guest"}}}}},
};
}
