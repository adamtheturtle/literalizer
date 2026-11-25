#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    -42,
    0,
    42,
    -1.25,
    0.0,
    1.25,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
