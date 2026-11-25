#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::array({}),
    nlohmann::json::array({}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
