#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::vector<int>{
    0xf4240,
    -0x4d2,
    0xff,
    -0xa,
};
}
