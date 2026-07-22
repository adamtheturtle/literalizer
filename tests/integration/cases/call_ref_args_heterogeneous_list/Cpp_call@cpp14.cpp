#include <initializer_list>
#include <vector>
#include <string>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_ints = std::vector<int>{
    1,
    2,
    3,
};
auto my_strings = std::vector<std::string>{
    "a",
    "b",
};
auto my_empty = std::vector<std::nullptr_t>{};
process(std::move(my_ints), 42);
process(std::move(my_strings), 7);
process(std::move(my_empty), 99);
    return 0;
}
