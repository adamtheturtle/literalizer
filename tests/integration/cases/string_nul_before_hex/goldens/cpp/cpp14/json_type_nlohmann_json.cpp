#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"x", std::string{"before"} + '\0' + "after"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
