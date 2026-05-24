#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json({"name": "Alice", "age": 30, "active": true})json", nullptr, false);
    (void)my_data;
    return 0;
}
