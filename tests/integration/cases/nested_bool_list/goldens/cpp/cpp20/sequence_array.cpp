#include <array>
int main() {
auto my_data = std::array<std::array<bool, 2>, 2>{
    std::array<bool, 2>{true, false},
    std::array<bool, 2>{true, true},
};
    (void)my_data;
    return 0;
}
