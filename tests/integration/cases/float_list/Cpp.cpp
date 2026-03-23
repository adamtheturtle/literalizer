#include <initializer_list>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<double>{
    1.1,
    2.2,
    3.3,
};
}
