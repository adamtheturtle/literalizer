#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::map<std::string, std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>{
    {"filled", std::make_tuple(1, "value")},
    {"empty", std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
