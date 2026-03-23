#include <initializer_list>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<double>{
    1,
    2.5,
    3,
};
}
