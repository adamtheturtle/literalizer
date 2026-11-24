#include <nlohmann/json.hpp>
#include <utility>
auto consume_widget(auto...) { return 0; }
int main() {
    try {
auto item = nlohmann::json(nullptr);
auto my_data = nlohmann::json(nullptr);
consume_widget(my_data);
my_data = std::move_if_noexcept(item);
consume_widget(my_data);
        return 0;
    } catch (...) {
        return 1;
    }
}
