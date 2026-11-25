#include <nlohmann/json.hpp>
#include <utility>
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
