#include <initializer_list>
#include <string>
#include <map>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = std::map<std::string, std::string>{
    {"key", "it's here"},  // a comment
};
}
