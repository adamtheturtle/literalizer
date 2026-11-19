#include <cstddef>
#include <vector>
#include <type_traits>
#include <iostream>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto item = std::vector<std::nullptr_t>{};
auto my_data = std::vector<std::common_type_t<decltype(item), decltype(item)>>{
    item,
    item,
};
std::cout << json(my_data).dump() << '\n';
    return 0;
}
