#include <initializer_list>
#include <vector>
struct thingType_ { [[nodiscard]] auto go(auto...) const { return 0; } };
const thingType_ thing;
int main() {
auto my_data = thing.go(std::vector<int>{1});
    (void)my_data;
    return 0;
}
