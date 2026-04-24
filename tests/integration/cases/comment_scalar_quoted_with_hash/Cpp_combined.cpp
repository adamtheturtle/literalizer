#include <initializer_list>
#include <string>
void check_() {
// note
const auto* my_data = "hello # world";
(void)my_data;
// note
my_data = "hello # world";
    (void)my_data;
}
