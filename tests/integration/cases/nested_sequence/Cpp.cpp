#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
}
