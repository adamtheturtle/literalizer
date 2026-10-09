#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json(// leading
1);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
