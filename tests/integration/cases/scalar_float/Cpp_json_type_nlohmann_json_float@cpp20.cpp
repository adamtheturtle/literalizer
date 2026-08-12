#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json(3.14);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
