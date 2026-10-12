#include <nlohmann/json.hpp>
auto consume(auto...) { return 0; }
int main() {
    try {
auto item = nlohmann::json("s");
consume(std::move(item));
        return 0;
    } catch (...) {
        return 1;
    }
}
