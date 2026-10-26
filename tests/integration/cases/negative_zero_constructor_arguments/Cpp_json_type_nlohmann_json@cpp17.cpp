#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    -0.0,
    0.0,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
