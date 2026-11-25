#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"__proto__", nlohmann::json::object({{"x", 1}})},
    {"ordinary", 2},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
