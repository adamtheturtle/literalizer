#include <nlohmann/json.hpp>
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
auto my_data = nlohmann::json::array({
    0,
});
consume_widget(my_data);
my_data = std::move(shared);
consume_widget(my_data);
        return 0;
    } catch (...) {
        return 1;
    }
}
