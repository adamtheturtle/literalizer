#include <initializer_list>
#include <cstddef>
auto main() -> int {
// note
auto my_data = nullptr;
(void)my_data;
// note
my_data = nullptr;
    (void)my_data;
    return 0;
}
