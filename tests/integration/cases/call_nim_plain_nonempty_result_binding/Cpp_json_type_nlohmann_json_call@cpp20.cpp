#include <nlohmann/json.hpp>
auto make_widget(auto...) { return 0; }
int main() {
    try {
auto my_data = make_widget(nlohmann::json::array({1}));
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
