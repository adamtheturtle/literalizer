#include <initializer_list>
#include <string>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::string>{
    "a",  // note a
    "b",  // note b
};
    (void)my_data;
    return 0;
}
