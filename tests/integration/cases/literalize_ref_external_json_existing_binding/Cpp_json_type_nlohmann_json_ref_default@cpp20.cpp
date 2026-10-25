#include <nlohmann/json.hpp>
auto consume_widget(auto...) { return 0; }
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"a", 0},
});
consume_widget(my_data);
my_data = nlohmann::json::object({
    {"a", 1},
});
consume_widget(my_data);
        return 0;
    } catch (...) {
        return 1;
    }
}
