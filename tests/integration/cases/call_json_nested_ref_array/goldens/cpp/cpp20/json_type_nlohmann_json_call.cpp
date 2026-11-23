#include <nlohmann/json.hpp>
auto consume(auto...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
consume(nlohmann::json::array({shared, 42}));
        return 0;
    } catch (...) {
        return 1;
    }
}
