#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    (-0x7fffffff - 1),
    -0x7fffffff,
    std::vector<int>{0x0},
};
    (void)my_data;
    return 0;
}
