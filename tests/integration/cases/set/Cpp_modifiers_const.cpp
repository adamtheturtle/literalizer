#include <initializer_list>
#include <string>
auto main() -> int {
const auto my_data = std::initializer_list<std::string>{
    "apple",
    "banana",
    "cherry",
};
    (void)my_data;
    return 0;
}
