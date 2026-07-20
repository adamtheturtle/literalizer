#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json({"name": "Alice", "scores": [10, 20, 30]})json", nullptr, false);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
