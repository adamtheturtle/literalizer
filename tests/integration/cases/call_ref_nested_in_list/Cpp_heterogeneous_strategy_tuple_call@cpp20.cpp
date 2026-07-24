#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
auto my_other = 7;
process(std::make_tuple(my_var, 42, "static"));
process(std::make_tuple(my_other, 7, "label"));
    return 0;
}
