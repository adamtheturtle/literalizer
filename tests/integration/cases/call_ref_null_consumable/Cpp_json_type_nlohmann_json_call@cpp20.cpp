#include <nlohmann/json.hpp>
auto consume(auto...) { return 0; }
int main() {
    try {
auto my_null = nlohmann::json(nullptr);
auto regular_null = nlohmann::json(nullptr);
consume(std::move(my_null));
consume(regular_null);
        return 0;
    } catch (...) {
        return 1;
    }
}
