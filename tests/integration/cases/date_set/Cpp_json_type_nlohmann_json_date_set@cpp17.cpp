#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json(["2024-01-15", "2024-06-01"])json", nullptr, false);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
