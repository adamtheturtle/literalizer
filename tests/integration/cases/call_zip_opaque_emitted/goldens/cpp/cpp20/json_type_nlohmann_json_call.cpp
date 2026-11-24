#include <nlohmann/json.hpp>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
    try {
emit(process(nlohmann::json(1)), nlohmann::json("2024-01-15T12:00:00"));
        return 0;
    } catch (...) {
        return 1;
    }
}
