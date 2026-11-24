#include <nlohmann/json.hpp>
template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
    try {
emit(process(nlohmann::json(1)), nlohmann::json("2024-01-15T12:00:00"));
        return 0;
    } catch (...) {
        return 1;
    }
}
