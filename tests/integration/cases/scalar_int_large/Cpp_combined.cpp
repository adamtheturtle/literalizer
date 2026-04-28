#include <initializer_list>
auto main() -> int {
auto my_data = 2147483648;
(void)my_data;
my_data = 2147483648;
    (void)my_data;
    return 0;
}
