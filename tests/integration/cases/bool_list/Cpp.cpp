#include <initializer_list>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<bool>{
    true,
    false,
    true,
};
}
