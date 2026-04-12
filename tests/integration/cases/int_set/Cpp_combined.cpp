#include <initializer_list>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
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
