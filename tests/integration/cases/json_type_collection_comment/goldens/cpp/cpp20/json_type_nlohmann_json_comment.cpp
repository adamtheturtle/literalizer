#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"a", 1},  // About a.
    {"b", 2},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
