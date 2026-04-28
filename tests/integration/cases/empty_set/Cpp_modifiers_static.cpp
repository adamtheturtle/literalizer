#include <initializer_list>
#include <cstddef>
auto main() -> int {
static auto my_data = std::initializer_list<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
