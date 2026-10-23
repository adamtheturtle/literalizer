#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
