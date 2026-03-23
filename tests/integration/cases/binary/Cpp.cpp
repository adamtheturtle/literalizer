#include <initializer_list>
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::string>{
    "48656c6c6f",
};
}
