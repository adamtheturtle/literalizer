#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json({"name": "Alice", "score": null, "age": 30})json");
    (void)my_data;
    return 0;
}
