#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"a", nlohmann::json::array({nlohmann::json::object({{"item", nlohmann::json::array({1})}})})},
    {"b", nlohmann::json::array({nlohmann::json::object({{"item", nlohmann::json::array({2, 3})}})})},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
