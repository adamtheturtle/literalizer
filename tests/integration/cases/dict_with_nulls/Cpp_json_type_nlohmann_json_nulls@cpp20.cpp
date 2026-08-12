#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
