#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json([
    [1, "a"],
    [2, "b"]
])json");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
