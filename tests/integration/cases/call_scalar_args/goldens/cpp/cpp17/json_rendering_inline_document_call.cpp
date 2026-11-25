#include <nlohmann/json.hpp>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
    try {
process(nlohmann::json::parse(R"json("hello")json"));
process(nlohmann::json::parse(R"json(42)json"));
process(nlohmann::json::parse(R"json(true)json"));
        return 0;
    } catch (...) {
        return 1;
    }
}
