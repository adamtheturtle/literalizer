#include <nlohmann/json.hpp>
auto process(auto...) { return 0; }
int main() {
    try {
auto unknown_value = nlohmann::json::array({});
process(nlohmann::json::array({unknown_value}));
        return 0;
    } catch (...) {
        return 1;
    }
}
