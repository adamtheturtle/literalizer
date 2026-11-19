#include <iostream>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto my_data = 0;
auto shared = 1;
std::cout << json(my_data).dump() << '\n';
my_data = shared;
std::cout << json(my_data).dump() << '\n';
    return 0;
}
