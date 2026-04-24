#include <initializer_list>
#include <vector>
#include <cstddef>
void check_() {
auto my_data = std::vector<std::nullptr_t>{};
(void)my_data;
my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
}
