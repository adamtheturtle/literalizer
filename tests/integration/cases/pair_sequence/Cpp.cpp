#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto main() -> int {
auto my_data = std::vector<std::variant<int, std::string>>{
    1,
    "hello",
};
    (void)my_data;
    return 0;
}
