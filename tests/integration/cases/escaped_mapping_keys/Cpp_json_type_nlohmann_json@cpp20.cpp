#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"quote\"backslash\\", 1},
    {"line\nbreak", 2},
    {"$(literal)${text}", 3},
    {"RStr prefix", 4},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
