#include <initializer_list>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.5, 2.5},
    std::vector<double>{3.5, 4.5},
};
    (void)my_data;
    return 0;
}
