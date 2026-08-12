#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"name", "Alice"},
    {"scores", nlohmann::json::array({10, 20, 30})},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
