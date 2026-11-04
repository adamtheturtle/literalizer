#include <cstddef>
#include <vector>
struct thingType_ { [[nodiscard]] auto go(auto...) const { return 0; } };
const thingType_ thing;
int main() {
auto my_data = thing.go(std::vector<std::nullptr_t>{});
    (void)my_data;
    return 0;
}
