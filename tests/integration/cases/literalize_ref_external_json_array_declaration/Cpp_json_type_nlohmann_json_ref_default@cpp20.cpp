#include <nlohmann/json.hpp>
#include <utility>
auto consume_widget(auto...) { return 0; }
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
auto&& my_data = std::move(shared);
consume_widget(my_data);
        return 0;
    } catch (...) {
        return 1;
    }
}
