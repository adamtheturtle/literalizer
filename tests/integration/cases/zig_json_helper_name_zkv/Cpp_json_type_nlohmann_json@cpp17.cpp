#include <nlohmann/json.hpp>
int main() {
    try {
auto ZKV = nlohmann::json::object({
    {"a", 1},
});
    (void)ZKV;
        return 0;
    } catch (...) {
        return 1;
    }
}
