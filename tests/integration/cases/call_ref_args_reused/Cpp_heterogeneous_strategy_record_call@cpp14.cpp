#include <initializer_list>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto single_var = std::vector<int>{
    4,
    5,
    6,
};
auto repeated_var = 1;
process(repeated_var, 1);
process(std::move(single_var), 0);
process(repeated_var, 8);
    return 0;
}
