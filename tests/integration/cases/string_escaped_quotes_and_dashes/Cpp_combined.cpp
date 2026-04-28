#include <initializer_list>
#include <string>
auto main() -> int {
const auto* my_data = "hello \"world\" -- not a comment";
(void)my_data;
my_data = "hello \"world\" -- not a comment";
    (void)my_data;
    return 0;
}
