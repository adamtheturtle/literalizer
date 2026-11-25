#include <nlohmann/json.hpp>
#include <cmath>
int main() {
    try {
auto my_data = nlohmann::json::array({
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
