#include <initializer_list>
#include <string>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = "hello \"world\" -- not a comment";
my_data = "hello \"world\" -- not a comment";
}
