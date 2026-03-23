#include <initializer_list>
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {std::vector<int>{1, 2}, std::vector<std::string>{"a", "b"}},
};
}
