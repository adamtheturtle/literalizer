#include <nlohmann/json.hpp>
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
auto&& my_data = shared;
(void)my_data;
my_data = shared;
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
