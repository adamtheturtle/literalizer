#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    (-0x7fffffff - 1),
    -0x7fffffff,
    std::vector<int>{0x0},
};
    (void)my_data;
    return 0;
}
