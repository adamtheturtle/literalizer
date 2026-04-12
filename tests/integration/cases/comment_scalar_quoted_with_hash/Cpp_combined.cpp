#include <initializer_list>
#include <string>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
// note
Any my_data = "hello # world";
// note
my_data = "hello # world";
}
