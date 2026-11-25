#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "issue #{42}",
    "color #red",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
