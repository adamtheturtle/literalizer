#include <nlohmann/json.hpp>
auto make_widget(auto...) { return 0; }
int main() {
    try {
auto value = nlohmann::json(1);
make_widget(value);
        return 0;
    } catch (...) {
        return 1;
    }
}
