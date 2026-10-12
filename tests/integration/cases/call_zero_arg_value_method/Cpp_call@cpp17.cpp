#include <initializer_list>
#include <vector>
#include <cstddef>
struct thingType_ { template <typename... Args> [[nodiscard]] auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
static_cast<void>(thing.go());
    return 0;
}
