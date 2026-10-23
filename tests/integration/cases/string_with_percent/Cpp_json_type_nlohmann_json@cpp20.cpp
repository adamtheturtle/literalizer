#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::array({
    "100% done",
    "%(name) is here",
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
