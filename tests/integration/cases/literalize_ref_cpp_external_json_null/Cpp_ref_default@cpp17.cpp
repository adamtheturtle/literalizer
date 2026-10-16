#include <nlohmann/json.hpp>
#include <utility>
int main() {
    try {
auto item = nlohmann::json(nullptr);
auto my_data = nlohmann::json(nullptr);
(void)my_data;
my_data = std::move(item);
(void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
