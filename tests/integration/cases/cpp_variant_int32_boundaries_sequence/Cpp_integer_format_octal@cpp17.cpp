#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    (-017777777777 - 1),
    -017777777777,
    std::vector<int>{0},
};
    (void)my_data;
    return 0;
}
