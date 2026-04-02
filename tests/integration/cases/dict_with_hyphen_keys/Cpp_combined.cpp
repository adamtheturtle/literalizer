#include <initializer_list>
#include <string>
#include <map>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::map<std::string, std::string>{
    {"my-key", "value1"},
    {"another-key", "value2"},
    {"normal_key", "value3"},
};
my_data = std::map<std::string, std::string>{
    {"my-key", "value1"},
    {"another-key", "value2"},
    {"normal_key", "value3"},
};
}
