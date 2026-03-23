#include <initializer_list>
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::string>{
    // line 1
    // line 2
    "a",
};
}
