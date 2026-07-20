#include <nlohmann/json.hpp>
auto process(auto...) { return 0; }
int main() {
    try {
process(nlohmann::json::parse(R"json("hello")json", nullptr, false));
process(nlohmann::json::parse(R"json(42)json", nullptr, false));
process(nlohmann::json::parse(R"json(true)json", nullptr, false));
        return 0;
    } catch (...) {
        return 1;
    }
}
