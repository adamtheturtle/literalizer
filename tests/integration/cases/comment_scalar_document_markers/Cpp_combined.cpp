#include <initializer_list>
void check_() {
auto my_data = // note
42;
(void)my_data;
my_data = // note
42;
    (void)my_data;
}
