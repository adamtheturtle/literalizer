#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
void check_() {
auto my_var = std::vector<int>{
    1,
    2,
    3,
};
process(my_var);
}
