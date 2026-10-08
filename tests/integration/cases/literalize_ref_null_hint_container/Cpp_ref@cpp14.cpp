#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
auto my_value = std::vector<int>{
    1,
    2,
};
auto my_data = std::move(my_value);
    (void)my_data;
    return 0;
}
