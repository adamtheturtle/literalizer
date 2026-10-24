#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"08", "value"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
