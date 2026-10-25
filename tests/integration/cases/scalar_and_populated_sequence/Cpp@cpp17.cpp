#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<int>>>{
    1,
    std::vector<int>{2, 3},
};
    (void)my_data;
    return 0;
}
