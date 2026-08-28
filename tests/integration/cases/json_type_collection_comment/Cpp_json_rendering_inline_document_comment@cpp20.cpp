#include <nlohmann/json.hpp>
int main() {
    try {
// About a.
auto my_data = nlohmann::json::parse(R"json({
    "a": 1,
    "b": 2
})json");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
