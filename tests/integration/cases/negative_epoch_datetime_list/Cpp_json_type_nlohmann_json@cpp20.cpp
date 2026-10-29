#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "1960-01-01T00:00:00+00:00",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
