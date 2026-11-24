#include <nlohmann/json.hpp>
auto process(auto...) { return 0; }
int main() {
    try {
process(nlohmann::json("hello"));
process(nlohmann::json(42));
process(nlohmann::json(true));
        return 0;
    } catch (...) {
        return 1;
    }
}
