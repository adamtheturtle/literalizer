#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<int>{
    0b0,
    0b1,
    -0b1,
};
    (void)my_data;
    return 0;
}
