#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
auto empty_values = std::vector<int>{};
auto integer_values = std::vector<int>{
    1,
};
auto my_data = std::vector<std::vector<int>>{
    std::move(empty_values),
    std::move(integer_values),
};
    (void)my_data;
    return 0;
}
