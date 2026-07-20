#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_var = std::vector<int>{
    1,
    2,
    3,
};
process(std::move(my_var));
    return 0;
}
