#include <initializer_list>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::vector<bool>>{
    std::vector<bool>{true, false},
    std::vector<bool>{true, true},
};
}
