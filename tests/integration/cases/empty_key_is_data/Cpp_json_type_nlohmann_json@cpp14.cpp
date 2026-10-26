#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::object({{"", "external_value"}}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
