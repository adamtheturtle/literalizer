#include <nlohmann/json.hpp>
#include <limits>
#include <cmath>
int main() {
    try {
auto my_data = nlohmann::json::array({std::numeric_limits<double>::infinity(), -std::numeric_limits<double>::infinity(), std::numeric_limits<double>::quiet_NaN()});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
