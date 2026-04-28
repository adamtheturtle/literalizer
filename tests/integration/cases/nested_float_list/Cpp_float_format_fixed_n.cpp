#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.500000, 2.500000},
    std::vector<double>{3.500000, 4.500000},
};
    (void)my_data;
    return 0;
}
