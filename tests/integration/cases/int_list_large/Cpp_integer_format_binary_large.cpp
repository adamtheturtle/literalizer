#include <initializer_list>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<int>{
    0b11110100001001000000,
    -0b10011010010,
    0b11111111,
    -0b1010,
};
}
