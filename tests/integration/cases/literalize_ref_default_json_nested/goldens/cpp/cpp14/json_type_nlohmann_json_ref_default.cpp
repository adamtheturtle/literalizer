#include <nlohmann/json.hpp>
int main() {
    try {
auto shared = nlohmann::json(42);
auto my_data = nlohmann::json::object({
    {"refs", nlohmann::json::array({shared, shared})},
    {"quoted", "#{shared}"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
