#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<double>{
    1,
    2.5,
    3,
};
(void)my_data;
my_data = std::vector<double>{
    1,
    2.5,
    3,
};
    (void)my_data;
    return 0;
}
