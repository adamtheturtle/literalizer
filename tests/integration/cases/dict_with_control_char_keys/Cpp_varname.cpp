#include <map>
#include <string>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::map<std::string, std::string>{
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
    {"", "value3"},
};
}
