#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json({"name": "Alice", "scores": [10, 20, 30]})json", nullptr, false);
(void)my_data;
my_data = nlohmann::json::parse(R"json({"name": "Alice", "scores": [10, 20, 30]})json", nullptr, false);
    (void)my_data;
    return 0;
}
