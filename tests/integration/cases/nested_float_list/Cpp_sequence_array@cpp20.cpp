#include <initializer_list>
#include <array>
#include <variant>
int main() {
auto my_data = std::array<std::array<double, 2>, 2>{
    std::array<double, 2>{1.5, 2.5},
    std::array<double, 2>{3.5, 4.5},
};
    (void)my_data;
    return 0;
}
