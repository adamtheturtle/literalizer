#include <nlohmann/json.hpp>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
consume(nlohmann::json::object({{"field", shared}, {"nested", nlohmann::json::array({shared, nlohmann::json::object({})})}}));
        return 0;
    } catch (...) {
        return 1;
    }
}
