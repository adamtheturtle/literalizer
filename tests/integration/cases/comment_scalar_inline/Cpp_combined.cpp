#include <initializer_list>
auto main() -> int {
// note
auto my_data = 42;
(void)my_data;
// note
my_data = 42;
    (void)my_data;
    return 0;
}
