#include <initializer_list>
#include <string>
void check_() {
const auto* my_data = "hello";
(void)my_data;
my_data = "hello";
    (void)my_data;
}
