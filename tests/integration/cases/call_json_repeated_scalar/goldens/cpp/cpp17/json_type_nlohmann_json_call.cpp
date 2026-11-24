#include <nlohmann/json.hpp>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json(42);
consume(nlohmann::json::array({shared, shared}));
        return 0;
    } catch (...) {
        return 1;
    }
}
