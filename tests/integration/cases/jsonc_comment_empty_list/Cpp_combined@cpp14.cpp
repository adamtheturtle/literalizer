#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
// empty heading
// empty body
// after empty
auto my_data = std::vector<std::nullptr_t>{};
(void)my_data;
// empty heading
// empty body
// after empty
my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
