#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json("2024-01-15T18:00:00+05:00");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
