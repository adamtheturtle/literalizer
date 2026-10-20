#include <initializer_list>
#include <vector>
#include <cstddef>
struct thingType_ { template <typename... Args> auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
auto my_data = thing.go(std::vector<std::nullptr_t>{});
    (void)my_data;
    return 0;
}
