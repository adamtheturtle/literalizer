#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json({"name": "Alice", "age": 30, "active": true})json");
    (void)my_data;
    return 0;
}
