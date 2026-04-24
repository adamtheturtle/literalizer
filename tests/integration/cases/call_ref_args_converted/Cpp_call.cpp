#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
void check_() {
auto my_var = std::vector<int>{
    1,
    2,
    3,
};
auto my_other = std::vector<int>{
    4,
    5,
    6,
};
process(my_var, 42);
process(my_other, 7);
}
