#include <initializer_list>
#include <vector>
#include <cstddef>
struct thingType_ { [[nodiscard]] auto go(auto...) const { return 0; } };
struct outerType_ { thingType_ thing; };
const outerType_ outer;
int main() {
static_cast<void>(outer.thing.go());
    return 0;
}
