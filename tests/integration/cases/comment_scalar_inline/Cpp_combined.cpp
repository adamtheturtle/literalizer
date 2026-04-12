#include <initializer_list>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
// note
Any my_data = 42;
// note
my_data = 42;
}
