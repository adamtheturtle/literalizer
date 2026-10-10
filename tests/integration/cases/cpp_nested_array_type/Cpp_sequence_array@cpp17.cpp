#include <initializer_list>
#include <array>
#include <variant>
int main() {
auto my_data = std::array<std::array<std::array<int, 1>, 1>, 1>{
    std::array<std::array<int, 1>, 1>{std::array<int, 1>{1}},
};
    (void)my_data;
    return 0;
}
