#include <nlohmann/json.hpp>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
    try {
static_cast<void>(make_widget(nlohmann::json::array({}), nlohmann::json::array({1}), nlohmann::json::array({})));
static_cast<void>(make_widget(nlohmann::json::array({"text"}), nlohmann::json::array({2}), nlohmann::json::array({})));
static_cast<void>(make_widget(nlohmann::json::array({}), nlohmann::json::array({"text"}), nlohmann::json::array({})));
static_cast<void>(make_widget(nlohmann::json::array({"text"}), nlohmann::json::array({2}), nlohmann::json::array({3})));
        return 0;
    } catch (...) {
        return 1;
    }
}
