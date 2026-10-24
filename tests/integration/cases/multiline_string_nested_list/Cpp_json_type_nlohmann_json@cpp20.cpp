#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    nlohmann::json::array({"\nfirst line\n  indented\n\nlast line\n"}),
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
