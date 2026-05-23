#include <nlohmann/json.hpp>
auto process(auto...) { return 0; }
int main() {
process(nlohmann::json::parse(R"json("hello")json"));
process(nlohmann::json::parse(R"json(42)json"));
process(nlohmann::json::parse(R"json(true)json"));
    return 0;
}
