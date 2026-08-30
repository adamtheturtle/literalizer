#include <initializer_list>
#include <vector>
int main() {
auto floating_value = 1.5;
auto integer_value = 2.0;
auto my_data = std::vector<double>{
    floating_value,
    integer_value,
};
    (void)my_data;
    return 0;
}
