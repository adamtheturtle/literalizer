#include <nlohmann/json.hpp>
auto make_widget(auto...) { return 0; }
int main() {
    try {
auto items = nlohmann::json::array({});
static_cast<void>(make_widget(items));
        return 0;
    } catch (...) {
        return 1;
    }
}
