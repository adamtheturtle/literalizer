#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct throttlerType_ { template <typename... Args> [[nodiscard]] auto check(Args...) const { return 0; } };
const throttlerType_ throttler;
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
    return 0;
}
