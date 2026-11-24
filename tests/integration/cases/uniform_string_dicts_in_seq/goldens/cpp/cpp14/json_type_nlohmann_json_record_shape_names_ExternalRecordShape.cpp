#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::object({{"first", "Alice"}, {"last", "Smith"}}),
    nlohmann::json::object({{"first", "Bob"}, {"last", "Jones"}}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
