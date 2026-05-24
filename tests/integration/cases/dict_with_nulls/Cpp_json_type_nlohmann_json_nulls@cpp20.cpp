#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json({"name": "Alice", "score": null, "age": 30})json", nullptr, false);
    (void)my_data;
    return 0;
}
