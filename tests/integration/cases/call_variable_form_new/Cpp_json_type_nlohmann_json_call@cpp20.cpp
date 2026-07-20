#include <nlohmann/json.hpp>
auto make_widget(auto...) { return 0; }
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json(42)json", nullptr, false);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
