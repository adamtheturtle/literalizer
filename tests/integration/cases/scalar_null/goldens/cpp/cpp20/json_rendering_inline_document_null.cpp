#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json(null)json");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
