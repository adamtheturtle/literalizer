#include <nlohmann/json.hpp>
auto consume(auto...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json(nullptr);
consume(nlohmann::json::object({{"left", shared}, {"nested", nlohmann::json::array({shared})}}));
        return 0;
    } catch (...) {
        return 1;
    }
}
