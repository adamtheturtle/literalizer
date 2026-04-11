#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = std::vector<int>{
    0,
    1,
    -1,
};
my_data = std::vector<int>{
    0,
    1,
    -1,
};
}
