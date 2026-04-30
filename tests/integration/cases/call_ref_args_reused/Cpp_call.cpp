#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
const auto single_var = std::vector<int>{
    4,
    5,
    6,
};
const auto repeated_var = 1;
process(repeated_var, 1);
process(single_var, 0);
process(repeated_var, 8);
    return 0;
}
