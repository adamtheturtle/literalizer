#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"$key", "a\"b\tcé #{world} $ident"},
    {"trailing multi-byte", "café"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
