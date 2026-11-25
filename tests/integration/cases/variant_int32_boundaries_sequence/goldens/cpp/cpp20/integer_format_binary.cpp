#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    (-0b1111111111111111111111111111111 - 1),
    -0b1111111111111111111111111111111,
    std::vector<int>{0b0},
};
    (void)my_data;
    return 0;
}
