#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"starts_at", "09:30:00"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
