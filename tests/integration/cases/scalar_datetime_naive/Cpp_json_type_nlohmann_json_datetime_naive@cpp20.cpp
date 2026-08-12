#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json("2024-01-15T12:30:00Z");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
