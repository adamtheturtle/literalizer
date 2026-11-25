#include <nlohmann/json.hpp>
int main() {
    try {
auto shared = nlohmann::json(42);
auto my_data = nlohmann::json::array({
    shared,
    shared,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
