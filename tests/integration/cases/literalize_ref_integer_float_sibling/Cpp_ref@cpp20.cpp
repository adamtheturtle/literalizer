#include <initializer_list>
#include <vector>
int main() {
auto integer_value = 1.0;
auto my_data = std::vector<double>{
    integer_value,
    1.5,
};
    (void)my_data;
    return 0;
}
