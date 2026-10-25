#include <nlohmann/json.hpp>
int main() {
    try {
        auto shared = nlohmann::json::array({
            1,
            2,
        });
        auto my_data = nlohmann::json::object({
            {"field", nlohmann::json::object({{"nested", std::move(shared)}})},
            {"text", "first\n{ \" // }"},
        });
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
