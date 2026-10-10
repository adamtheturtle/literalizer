#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::array({1, "a"}),
    nlohmann::json::array({2, "b"}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
