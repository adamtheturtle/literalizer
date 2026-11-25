#include <nlohmann/json.hpp>
#include <utility>
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
auto my_data = nlohmann::json::array({
    std::move(shared),
    42,
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
