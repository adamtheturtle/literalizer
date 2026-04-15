#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::vector<int>{
    1'000'000,
    -1'234,
    255,
    -10,
};
}
