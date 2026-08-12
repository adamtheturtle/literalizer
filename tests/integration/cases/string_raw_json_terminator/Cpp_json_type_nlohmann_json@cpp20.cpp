#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json::object({{")json", "x"}});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
