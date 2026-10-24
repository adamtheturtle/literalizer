#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"test", nlohmann::json::array({5, nlohmann::json::array({"compile", "test"})})},
    {"package", nlohmann::json::array({7, nlohmann::json::array({"link", "test"})})},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
