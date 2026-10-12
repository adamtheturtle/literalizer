#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    (-2147483647 - 1),
    -2147483647,
    std::vector<int>{0},
};
    (void)my_data;
    return 0;
}
