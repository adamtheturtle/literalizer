#include <nlohmann/json.hpp>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
    try {
auto value = nlohmann::json(1);
make_widget(value);
        return 0;
    } catch (...) {
        return 1;
    }
}
