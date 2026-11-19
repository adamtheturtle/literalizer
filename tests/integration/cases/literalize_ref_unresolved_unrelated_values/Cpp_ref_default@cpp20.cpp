#include <utility>
#include <vector>
#include <cstdlib>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto a = 0;
auto my_data = std::vector<int>{
    std::move_if_noexcept(a),
    1,
};
(json(my_data) == json::parse("[0, 1]") ? static_cast<void>(0) : std::abort());
    return 0;
}
