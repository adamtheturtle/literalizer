#include <initializer_list>
#include <vector>
#include <cstddef>
auto main() -> int {
auto my_data = std::vector<std::nullptr_t>{};
(void)my_data;
my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
