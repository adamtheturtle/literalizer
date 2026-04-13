#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
auto process(auto...) { return 0; }
void check_() {
process("hello");
process(42);
process(true);
}
