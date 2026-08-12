#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json::object({{"outer", nlohmann::json::object({{"alpha", 1}, {"beta", "two"}})}});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
