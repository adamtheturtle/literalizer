#include <nlohmann/json.hpp>
#include <cmath>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json([Infinity, -Infinity, NaN])json", nullptr, false);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
