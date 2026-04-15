#include <initializer_list>
#include <string>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
// note
auto my_data = "hello # world";
// note
my_data = "hello # world";
}
