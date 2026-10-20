#include <nlohmann/json.hpp>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
    try {
auto item = nlohmann::json("s");
consume(std::move(item));
        return 0;
    } catch (...) {
        return 1;
    }
}
