#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json([{"first": "Alice", "last": "Smith"}, {"first": "Bob", "last": "Jones"}])json", nullptr, false);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
