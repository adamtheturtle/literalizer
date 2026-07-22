#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_var = 42;
process(std::make_tuple(my_var, 42, "static"));
    return 0;
}
