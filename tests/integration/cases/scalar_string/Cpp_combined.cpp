#include <initializer_list>
#include <string>
auto main() -> int {
const auto* my_data = "hello";
(void)my_data;
my_data = "hello";
    (void)my_data;
    return 0;
}
