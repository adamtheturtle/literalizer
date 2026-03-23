#include <initializer_list>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::vector<double>>{
    std::vector<double>{1.5, 2.5},
    std::vector<double>{3.5, 4.5},
};
}
