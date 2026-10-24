#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"outer", nlohmann::json::array({nlohmann::json::array({"nested first line\n  indented\n\nnested last line\n"})})},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
