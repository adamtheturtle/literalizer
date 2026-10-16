#include <nlohmann/json.hpp>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
    try {
auto my_data = make_widget(nlohmann::json::array({}));
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
