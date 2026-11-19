#include <cstdlib>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto my_data = 0;
auto shared = 1;
(json(my_data) == json::parse("0") ? static_cast<void>(0) : std::abort());
my_data = shared;
(json(my_data) == json::parse("1") ? static_cast<void>(0) : std::abort());
    return 0;
}
