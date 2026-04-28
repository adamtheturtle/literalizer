#include <initializer_list>
#include <string>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::string>{
    "48656c6c6f",
};
(void)my_data;
my_data = std::vector<std::string>{
    "48656c6c6f",
};
    (void)my_data;
    return 0;
}
