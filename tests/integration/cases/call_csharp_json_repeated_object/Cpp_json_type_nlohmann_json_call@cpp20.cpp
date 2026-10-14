#include <nlohmann/json.hpp>
auto consume(auto...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json::object({
    {"value", nlohmann::json::array({1, 2})},
});
consume(nlohmann::json::object({{"left", shared}, {"right", shared}}));
        return 0;
    } catch (...) {
        return 1;
    }
}
