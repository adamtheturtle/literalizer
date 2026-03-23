#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
}
