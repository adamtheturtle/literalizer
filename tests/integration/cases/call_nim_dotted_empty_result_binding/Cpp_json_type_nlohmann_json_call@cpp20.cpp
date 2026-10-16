#include <nlohmann/json.hpp>
struct thingType_ { [[nodiscard]] auto go(auto...) const { return 0; } };
const thingType_ thing;
int main() {
    try {
auto my_data = thing.go(nlohmann::json::array({}));
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
