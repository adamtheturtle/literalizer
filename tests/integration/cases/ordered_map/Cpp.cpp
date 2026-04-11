#include <initializer_list>
#include <string>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
}
