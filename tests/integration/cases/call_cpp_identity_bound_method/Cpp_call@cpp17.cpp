#include <initializer_list>
#include <vector>
struct thingType_ { template <typename... Args> [[nodiscard]] auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
auto item = std::vector<int>{
    1,
    2,
};
static_cast<void>(thing.go(item));
    return 0;
}
