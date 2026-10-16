#include <nlohmann/json.hpp>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
    try {
auto items = nlohmann::json::array({});
static_cast<void>(make_widget(items));
        return 0;
    } catch (...) {
        return 1;
    }
}
