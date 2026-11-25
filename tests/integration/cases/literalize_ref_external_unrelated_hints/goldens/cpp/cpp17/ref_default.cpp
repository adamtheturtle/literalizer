#include <vector>
#include <utility>
#include <cstdlib>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto missing = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move_if_noexcept(missing);
([&]() noexcept {
    try {
        return json(my_data) == json::parse("[1, 2]");
    } catch (...) {
        return false;
    }
}() ? static_cast<void>(0) : std::abort());
    return 0;
}
