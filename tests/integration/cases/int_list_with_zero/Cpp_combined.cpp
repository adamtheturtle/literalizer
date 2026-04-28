#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<int>{
    0,
    1,
    -1,
};
(void)my_data;
my_data = std::vector<int>{
    0,
    1,
    -1,
};
    (void)my_data;
    return 0;
}
