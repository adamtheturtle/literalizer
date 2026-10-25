#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"within_i32", "2024-01-15T12:00:00"},
    {"beyond_i32", "2099-06-15T08:30:00"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
