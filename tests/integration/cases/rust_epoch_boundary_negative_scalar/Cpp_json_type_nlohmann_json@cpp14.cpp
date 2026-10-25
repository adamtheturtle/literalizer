#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json("1901-12-13T20:45:51");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
