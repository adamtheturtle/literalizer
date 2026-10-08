#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
auto empty_values = std::vector<double>{};
auto integer_values = std::vector<double>{
    1,
};
auto float_values = std::vector<double>{
    1.5,
};
auto my_data = std::vector<std::vector<double>>{
    std::move(empty_values),
    std::move(integer_values),
    std::move(float_values),
};
    (void)my_data;
    return 0;
}
