#include <initializer_list>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
