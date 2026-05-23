#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json({"name": "Alice", "scores": [10, 20, 30]})json");
(void)my_data;
my_data = nlohmann::json::parse(R"json({"name": "Alice", "scores": [10, 20, 30]})json");
    (void)my_data;
    return 0;
}
