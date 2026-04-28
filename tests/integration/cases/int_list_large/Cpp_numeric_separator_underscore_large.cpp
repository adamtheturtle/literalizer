#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<int>{
    1'000'000,
    -1'234,
    255,
    -10,
};
    (void)my_data;
    return 0;
}
