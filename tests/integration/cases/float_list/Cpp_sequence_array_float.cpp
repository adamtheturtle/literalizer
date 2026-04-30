#include <initializer_list>
#include <array>
int main() {
const auto my_data = std::array<double, 3>{
    1.1,
    -2.2,
    3.3,
};
    (void)my_data;
    return 0;
}
