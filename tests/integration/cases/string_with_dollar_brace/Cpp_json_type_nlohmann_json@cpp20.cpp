#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "prefix ${HOME} suffix",
    "${interpolated}",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
