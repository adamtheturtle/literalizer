#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::string>{
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
};
}
