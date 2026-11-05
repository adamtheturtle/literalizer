#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"morning", "09:30:00"},
    {"afternoon", "14:15:00"},
    {"evening", "23:59:59"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
