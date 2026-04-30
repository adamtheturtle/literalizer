#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto repeated_var = 1;
auto single_var = std::vector<int>{
    4,
    5,
    6,
};
process(repeated_var, 1);
process(std::move(single_var), 0);
process(repeated_var, 8);
    return 0;
}
