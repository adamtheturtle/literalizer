#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"a", 9223372036854775807},
    {"b", 9223372036854775808ULL},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
