#include <nlohmann/json.hpp>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
    try {
make_widget(nlohmann::json(1));
        return 0;
    } catch (...) {
        return 1;
    }
}
