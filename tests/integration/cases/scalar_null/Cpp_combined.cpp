#include <initializer_list>
#include <cstddef>
auto main() -> int {
auto my_data = nullptr;
(void)my_data;
my_data = nullptr;
    (void)my_data;
    return 0;
}
