#include <initializer_list>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<std::vector<bool>>{
    std::vector<bool>{true, false},
    std::vector<bool>{true, true},
};
my_data = std::vector<std::vector<bool>>{
    std::vector<bool>{true, false},
    std::vector<bool>{true, true},
};
}
