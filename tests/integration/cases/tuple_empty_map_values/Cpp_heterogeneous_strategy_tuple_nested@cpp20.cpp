#include <cstddef>
#include <map>
#include <string>
#include <tuple>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>{
    {"filled", std::make_tuple(1, "value")},
    {"empty", std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
