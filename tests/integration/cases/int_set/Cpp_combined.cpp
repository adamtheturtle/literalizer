#include <initializer_list>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    1,
    2,
    3,
};
my_data = {
    1,
    2,
    3,
};
}
