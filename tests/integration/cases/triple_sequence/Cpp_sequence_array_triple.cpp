#include <initializer_list>
#include <string>
#include <array>
void _check() {
    [[maybe_unused]] _Any _v = std::array<std::string, 3>{
    "1",
    "hello",
    "True",
};
}
