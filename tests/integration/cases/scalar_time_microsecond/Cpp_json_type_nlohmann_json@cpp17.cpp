#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"exact_millisecond", "09:30:15.123000"},
    {"sub_millisecond", "09:30:15.123456"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
