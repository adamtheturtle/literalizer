#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
