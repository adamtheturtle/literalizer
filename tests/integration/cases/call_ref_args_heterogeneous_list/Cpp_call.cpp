#include <initializer_list>
#include <vector>
#include <string>
#include <variant>
auto process(auto...) { return 0; }
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
process(std::move(my_ints), 42);
process(std::move(my_strings), 7);
    return 0;
}
