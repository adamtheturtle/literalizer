#include <nlohmann/json.hpp>
auto make_widget(auto...) { return 0; }
int main() {
    try {
make_widget(nlohmann::json(1));
        return 0;
    } catch (...) {
        return 1;
    }
}
