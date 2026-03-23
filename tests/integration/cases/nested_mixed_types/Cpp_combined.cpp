#include <string>
#include <vector>
void _check() {
auto my_data = {
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
my_data = {
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
}
