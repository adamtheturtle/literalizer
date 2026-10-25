#include <nlohmann/json.hpp>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
    try {
auto untyped_value = nlohmann::json::array({});
process(nlohmann::json::array({untyped_value, untyped_value}));
        return 0;
    } catch (...) {
        return 1;
    }
}
