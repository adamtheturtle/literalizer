#include <initializer_list>
#include <string>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::string>{
    "a",
    // trailing
};
(void)my_data;
my_data = std::vector<std::string>{
    "a",
    // trailing
};
    (void)my_data;
    return 0;
}
