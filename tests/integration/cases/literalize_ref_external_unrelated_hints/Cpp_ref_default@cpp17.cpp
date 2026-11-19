#include <vector>
#include <utility>
#include <iostream>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto missing = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move_if_noexcept(missing);
std::cout << json(my_data).dump() << '\n';
    return 0;
}
