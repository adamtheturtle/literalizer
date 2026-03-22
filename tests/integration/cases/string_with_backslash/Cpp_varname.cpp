#include <string>
#include <vector>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<std::string>{
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
};
}
