#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json("2099-06-15T08:30:00");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
