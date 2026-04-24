#include <initializer_list>
#include <cstddef>
void check_() {
// note
auto my_data = nullptr;
(void)my_data;
// note
my_data = nullptr;
    (void)my_data;
}
