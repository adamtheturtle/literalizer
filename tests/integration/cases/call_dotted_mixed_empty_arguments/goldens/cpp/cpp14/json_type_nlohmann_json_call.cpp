#include <nlohmann/json.hpp>
struct thingType_ { template <typename... Args> auto go(Args...) const { return 0; } };
const thingType_ thing;
int main() {
    try {
static_cast<void>(thing.go(nlohmann::json::array({}), nlohmann::json::array({1}), nlohmann::json::array({})));
static_cast<void>(thing.go(nlohmann::json::array({"text"}), nlohmann::json::array({2}), nlohmann::json::array({})));
static_cast<void>(thing.go(nlohmann::json::array({}), nlohmann::json::array({"text"}), nlohmann::json::array({})));
static_cast<void>(thing.go(nlohmann::json::array({"text"}), nlohmann::json::array({2}), nlohmann::json::array({3})));
        return 0;
    } catch (...) {
        return 1;
    }
}
