#include <cstddef>
#include <vector>
#include <type_traits>
#include <cstdlib>
#include <nlohmann/json.hpp>
using nlohmann::json;
int main() {
auto item = std::vector<std::nullptr_t>{};
auto my_data = std::vector<std::common_type_t<decltype(item), decltype(item)>>{
    item,
    item,
};
([&]() noexcept {
    try {
        return json(my_data) == json::parse("[[], []]");
    } catch (...) {
        return false;
    }
}() ? static_cast<void>(0) : std::abort());
    return 0;
}
