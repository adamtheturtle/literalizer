#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json(9223372036854775808);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
