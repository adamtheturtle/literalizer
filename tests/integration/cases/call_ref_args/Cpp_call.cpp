#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
const auto my_var = std::vector<int>{
    1,
    2,
    3,
};
const auto my_other = std::vector<int>{
    4,
    5,
    6,
};
process(my_var, 42);
process(my_other, 7);
    return 0;
}
