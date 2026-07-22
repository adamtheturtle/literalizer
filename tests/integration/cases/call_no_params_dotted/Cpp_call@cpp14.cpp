#include <initializer_list>
#include <vector>
struct throttlerType_ { template <typename... Args> void check(Args...) const {} };
const throttlerType_ throttler;
int main() {
throttler.check();
throttler.check();
    return 0;
}
