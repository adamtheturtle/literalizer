#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json(42)json");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
