#include <nlohmann/json.hpp>
int main() {
    try {
auto arena = nlohmann::json::object({
    {"a", 1},
});
    (void)arena;
        return 0;
    } catch (...) {
        return 1;
    }
}
