#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "48656c6c6f",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
