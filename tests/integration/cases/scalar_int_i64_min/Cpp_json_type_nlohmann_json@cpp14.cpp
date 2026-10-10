#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json((-9223372036854775807LL - 1));
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
