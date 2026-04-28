#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
auto main() -> int {
auto my_var = std::vector<int>{
    1,
    2,
    3,
};
process(my_var);
    return 0;
}
