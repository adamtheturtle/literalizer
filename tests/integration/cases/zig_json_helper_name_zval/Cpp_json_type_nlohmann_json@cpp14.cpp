#include <nlohmann/json.hpp>
int main() {
    try {
auto ZVal = nlohmann::json::object({
    {"a", 1},
});
    (void)ZVal;
        return 0;
    } catch (...) {
        return 1;
    }
}
