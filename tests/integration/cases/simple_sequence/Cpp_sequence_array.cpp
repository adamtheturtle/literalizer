#include <initializer_list>
#include <string>
#include <cstddef>
#include <array>
void _check() {
    [[maybe_unused]] _Any _v = std::array<std::string, 4>{
    "1",
    "hello",
    "True",
    "None",
};
}
