#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    5.0e-324,
    -5.0e-324,
    1.0e-310,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
