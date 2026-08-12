#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json::object({{"name", "Alice"}, {"age", 30}, {"active", true}});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
