#include <utility>
#include <vector>
#include <iostream>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto a = 0;
auto my_data = std::vector<int>{
    std::move_if_noexcept(a),
    1,
};
std::cout << json(my_data).dump() << '\n';
    return 0;
}
