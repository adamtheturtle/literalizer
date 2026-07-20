#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
struct throttlerType_ { template <typename... Args> void check(Args...) const {} };
const throttlerType_ throttler;
int main() {
throttler.check();
throttler.check();
    return 0;
}
