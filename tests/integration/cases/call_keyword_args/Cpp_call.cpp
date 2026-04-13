#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
struct throttlerType_ { auto check(auto...) const { return 0; } };
const throttlerType_ throttler;
auto emit(auto...) { return 0; }
void check_() {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
}
