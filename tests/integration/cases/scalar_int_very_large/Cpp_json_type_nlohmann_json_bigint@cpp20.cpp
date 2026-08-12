#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json(nlohmann::json::number_unsigned_t{9223372036854775808ULL});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
