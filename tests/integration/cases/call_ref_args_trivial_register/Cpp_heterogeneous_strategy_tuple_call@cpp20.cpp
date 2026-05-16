#include <initializer_list>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto my_int = 1;
auto my_bool = true;
auto my_float = 3.14;
auto my_list = std::vector<int>{
    1,
    2,
    3,
};
process(my_int, 42);
process(my_bool, 7);
process(my_float, 9);
process(std::move(my_list), 1);
    return 0;
}
