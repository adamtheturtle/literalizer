#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "price $10",
    "$HOME",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
