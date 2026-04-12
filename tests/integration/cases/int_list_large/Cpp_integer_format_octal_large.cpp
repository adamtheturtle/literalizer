#include <initializer_list>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<int>{
    03641100,
    -02322,
    0377,
    -012,
};
}
