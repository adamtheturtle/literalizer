#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::object({{"values", nlohmann::json::array({})}}),
    nlohmann::json::object({}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
