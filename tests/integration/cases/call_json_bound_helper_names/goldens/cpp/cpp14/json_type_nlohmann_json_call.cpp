#include <nlohmann/json.hpp>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
    try {
auto arena = nlohmann::json::object({
    {"a", 1},
});
auto ZVal = nlohmann::json::object({
    {"a", 1},
});
auto ZKV = nlohmann::json::object({
    {"a", 1},
});
process(arena);
process(ZVal);
process(ZKV);
        return 0;
    } catch (...) {
        return 1;
    }
}
