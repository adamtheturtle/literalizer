#include <initializer_list>
#include <string>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = {
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
my_data = {
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
}
