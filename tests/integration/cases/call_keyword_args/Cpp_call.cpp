#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct throttlerType_ { auto check(auto...) const { return 0; } };
const throttlerType_ throttler;
auto emit(auto...) { return 0; }
auto main() -> int {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
    return 0;
}
