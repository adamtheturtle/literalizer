#include <cstdlib>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto my_data = 0;
auto shared = 1;
([&]() noexcept {
    try {
        return json(my_data) == json::parse("0");
    } catch (...) {
        return false;
    }
}() ? static_cast<void>(0) : std::abort());
my_data = shared;
([&]() noexcept {
    try {
        return json(my_data) == json::parse("1");
    } catch (...) {
        return false;
    }
}() ? static_cast<void>(0) : std::abort());
    return 0;
}
