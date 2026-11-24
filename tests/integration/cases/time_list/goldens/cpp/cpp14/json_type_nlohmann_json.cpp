#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"times", nlohmann::json::array({"09:30:00", "17:45:00", "23:59:59"})},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
