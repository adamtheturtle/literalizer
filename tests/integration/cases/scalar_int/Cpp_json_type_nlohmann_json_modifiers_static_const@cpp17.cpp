#include <nlohmann/json.hpp>
int main() {
    try {
static const auto my_data = nlohmann::json(42);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
