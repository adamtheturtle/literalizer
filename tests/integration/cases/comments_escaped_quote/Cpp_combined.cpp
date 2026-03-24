#include <initializer_list>
#include <string>
#include <map>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
}
